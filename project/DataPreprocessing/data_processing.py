"""
새로운 파일이 추가되었을 때 실행되어,
MySQL DB에 추가된 데이터를 넣는 모듈
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import re

import argparse
import mysql.connector

from pprint import pprint
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine


# 오픈 소스 클래스를 상속받아 따로 만든 클래스. 내부에 함수를 추가하여 따로 정의된 레이아웃에 맡게 텍스트를 변환하도록 함. 
class PDFPageDetailedAggregator(PDFPageAggregator):
    def __init__(self, rsrcmgr, pageno=1, laparams=None):
        PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.rows = []
        self.page_number = 0
        self.stop = 0

    def receive_layout(self, ltpage):
        def render(item, page_number):
            if isinstance(item, LTPage) or isinstance(item, LTTextBox):
                for child in item:
                    render(child, page_number)
            elif isinstance(item, LTTextLine):
                child_str = ''
                for child in item:
                    if isinstance(child, (LTChar, LTAnno)):
                        child_str += child.get_text()
                child_str = ' '.join(child_str.split()).strip()
                if child_str: # 정규식을 통한 페이지 번호 및 목차 번호 삭제
                    m = re.match("^([–-])?(\s)?(([0-9]|[iIvVxX]){1,3})(\s)?([–-])?$", child_str.strip())
                    if not m:
                        row = (page_number, item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3],
                               child_str)  # bbox == (x1, y1, x2, y2)
                        self.rows.append(row)
                for child in item:
                    render(child, page_number)
            return

        render(ltpage, self.page_number)
        self.page_number += 1
        self.rows = sorted(self.rows, key=lambda x: (x[0], -x[2]))
        self.result = ltpage

    def delete_rows(self):
        self.rows = []

# 커버 페이지에서 필요한 부분을 가져오기 위한 함수. 정규식 사용
def cover_parser(rows):
    title = ""
    author = ""
    school = "Pohang University of Science and Technology"
    year = ""
    degree = ""
    department = "Computer Science and Engineering"

    re_degree = re.compile('Doctor|Master')
    re_author = re.compile('\(')
    re_department = re.compile('Department of|Division of')
    re_year = re.compile('^[0-9]{4}$')

    step = 0
    for i, r in enumerate(rows):
        if step == 0:
            m = re_degree.match(r)
            if m:
                degree = m.group()
                step += 1
        elif step == 1:
            m = re_department.match(rows[i + 1])
            if m:
                n = re_author.search(r)
                if n:
                    author = r[:n.start()]
                else:
                    author = r
                step += 1
            else:
                title += r + " "
        elif step == 2:
            m = re_year.match(r)
            if m:
                year = m.group()
                step += 1
        elif step == 3:
            break

    return (title, author, school, year, degree, department)

# abstract 부분을 가져오기 위한 함수. 커버 페이지 이후에 abstract가 나오는 것을 활용.
def abstract_parser(rows):
    abstract = " "

    re_abstract = re.compile('(.+)?(Abstract|ABSTRACT)$')
    re_content = re.compile('Contents$')

    step = 0
    font_size = 0
    for i, r in enumerate(rows):
        if step == 0:
            m = re_abstract.match(r[-1])
            if m:
                step += 1
                font_size = rows[i + 1][4] - rows[i + 1][2] + 0.2
        elif step == 1:
            if r[4] - r[2] > font_size and re_content.search(r[-1]):
                step += 1
            else:
                if abstract[-1] == "-":
                    abstract = abstract[:-1] + r[-1]
                else:
                    abstract += " " + r[-1]
        else:
            return abstract

    return False



def main():
    connection = mysql.connector.connect(
        host="52.79.166.26",
        port=3306,
        user="csed232",
        passwd="csed232",
        database="postech",
        auth_plugin="mysql_native_password"
    )

    cursor = connection.cursor()


    # currnet file directory
    wd = os.getcwd()

    # check new data in the dataset
    files = [(i, name) for i, name in enumerate(os.listdir("../dashboard-nodejs/uploads"))]

    input_data = []
    for i, file in enumerate(files):
        pdf = open(os.path.join("../dashboard-nodejs/uploads", file[1]), 'rb')
        parser = PDFParser(pdf)
        doc = PDFDocument(parser)

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        title = ""
        author = ""
        school = ""
        publisher = "General Graduate School"
        year = ""
        degree = ""
        department = ""
        abstract = ""

        page_num = 0
        # 첫 페이지는 안내문이므로 넘어가고, 이후 커버 페이지에서 정보를 뺴오고 바로 abstract를 찾고 멈춘다.
        for page in PDFPage.create_pages(doc):
            page_num += 1
            if page_num == 1:
                continue
            interpreter.process_page(page)
            # receive the LTPage object for this page
            device.get_result()
            if page_num == 2:
                title, author, school, year, degree, department = cover_parser([r[-1] for r in device.rows])
                device.delete_rows()
            else:
                abstract = abstract_parser(device.rows)
                if abstract:
                    break
                else:
                    continue
        # DB에 저장하는 부분
        query = ("SELECT COUNT(*) FROM paper;")
        cursor.execute(query)
        data = cursor.fetchall()

        query = ("INSERT INTO paper(id, degree, title, author, school, publisher, year, department, abstract) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)")

        cursor.execute(query, (data[0][0], degree, title, author, school, publisher, year, department, abstract))

        connection.commit()

    print(input_data)

    return 0


if __name__ == '__main__':
    main()

