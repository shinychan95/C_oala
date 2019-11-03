import pandas as pd
from pyhive import presto
import re
import os
import sys
import dha
import ahocorasick
import numpy as np
import csv
import ast
import operator
import pandas as pd
import ast
import time

# News Data Class
class NewsDataTable:
    # 특정 뉴스 아이디를 입력받으면, 뉴스 타이틀과 본문을 반환하기 위한 클래스
    def __init__(self, host='media-doraemon-presto01.dakao.io', port=8080, schema='mimi', username='cody.bright'):
        conn = presto.connect(host=host,
                              port=port,
                              schema=schema,
                              username=username)
        query = """
                      SELECT newsid,
                             title,
                             sentences
                      FROM hive.tmp.cody_region_news
                      WHERE dt
                          BETWEEN '20181122'
                              AND '20181228'
                """
        col = ['newsid', 'title', 'sentences']
        cursor = conn.cursor()
        cursor.execute(query)
        self.news = pd.DataFrame(cursor.fetchall(), columns=col)

    def query_filtering(self, query_data):
        self.news = pd.merge(self.news, query_data.query[['newsid']].drop_duplicates().reset_index(drop=True), on=['newsid'])

    def get_title(self, newsid):
        return self.news.loc[self.news['newsid'] == newsid, ['title']].iloc[0, 0]

    def get_sentences(self, newsid):
        return self.news.loc[self.news['newsid'] == newsid, ['sentences']].iloc[0, 0]


# Keyword Data Class
class QueryDataTable:
    # row = [dt, query, newsid, pv]

    def __init__(self, host='media-doraemon-presto01.dakao.io', port=8080, schema='mimi', username='cody.bright'):
        conn = presto.connect(host=host,
                              port=port,
                              schema=schema,
                              username=username)
        # 일주일 통으로 뽑을지 아니면 날마다 데이터 적재 후 합칠지
        query = """ 
                    SELECT query,
                         newsid,
                         count(*) AS pv
                    FROM hive.tmp.cody_search_query_news
                    WHERE dt
                      BETWEEN '20181222'
                          AND '20181228'
                    GROUP BY  query, newsid
                """
        col = ['query', 'newsid', 'pv']
        cursor = conn.cursor()
        cursor.execute(query)
        self.query = pd.DataFrame(cursor.fetchall(), columns=col)
        self.query['query'] = self.query['query'].str.replace(' ', '')
        self.query['query'] = self.query['query'].str.lower()
        self.query['query'] = self.query['query'].replace('[-=.#/?:${}]', '', regex=True)

    def news_filtering(self, news_data):
        self.query = pd.merge(self.query, news_data.news[['newsid']], on=['newsid'])


    def quark_filtering(self, quark_data):
        self.query = pd.merge(self.query, quark_data, on=['query'])


# Region Data Class
class RegionDataTable:
    # row = [nname, depth, above]

    def __init__(self, host='media-doraemon-presto01.dakao.io', port=8080, schema='mimi', username='cody.bright'):
        conn = presto.connect(host=host,
                              port=port,
                              schema=schema,
                              username=username)
        query = """
                    SELECT nname AS region,
                             ndepth,   
                        CASE WHEN nname4 is NOT NULL THEN nname3
                        WHEN nname3 is NOT NULL THEN nname2
                        WHEN nname2 is NOT NULL THEN nname1
                        ELSE NULL END AS upward,
                        CASE WHEN nsynonym3 is NOT NULL THEN nsynonym3
                        WHEN nsynonym2 is NOT NULL THEN nsynonym2
                        WHEN nsynonym1 is NOT NULL THEN nsynonym1
                        ELSE NULL END AS synonyms
                    FROM place.loc_region
                    WHERE regexp_like(nname, '^[가-힣]+$')
                            AND ((depth = 1 AND (length(nname) = 2 OR length(nname) = 7))
                                OR (depth = 2 AND nname != '세종특별자치시')
                                )
                    ORDER BY  ndepth ASC
        
                """
        col = ['region', 'ndepth', 'upward', 'synonyms']
        cursor = conn.cursor()
        cursor.execute(query)
        self.region = pd.DataFrame(cursor.fetchall(), columns=col)
        # 'depth'의 경우 'int'로 데이터 형을 바꾼다.
        self.region['ndepth'] = self.region['ndepth'].astype(int)


        for index in range(len(self.region)):
            tmp = self.region.loc[index, 'synonyms'].split(';')
            tmp = list(set(tmp))
            tmp = self.__delDuplicated(tmp)
            self.region.loc[index, 'synonyms'] = tmp

        self.region_data_modify()


    def make_synonym_upward_dict(self, region_data):
        self.synonym_dict = {}
        self.upward_dict = {}
        self.ambiguous_list = []
        for index in range(len(region_data)):
            tmp = region_data.loc[index, 'synonyms'].split(';')
            for x in tmp:
                if x in self.synonym_dict:
                    self.ambiguous_list.append(x)
                    self.upward_dict[x].append(region_data.loc[index, 'upward'])
                    if region_data.loc[index, 'region'] in self.synonym_dict[x]:
                        pass
                    else:
                        self.synonym_dict[x].append(region_data.loc[index, 'region'])
                else:
                    self.synonym_dict[x] = [region_data.loc[index, 'region']]
                    self.upward_dict[x] = [region_data.loc[index, 'upward']]


    def get_all_synonyms(self, region_data):
        result = []
        for synonyms in region_data['synonyms']:
            result += synonyms.split(';')
        return list(set(result))


    def get_decide_region(self):
        return list(self.region[self.region['ndepth'] == 1]['region'])+list(set(self.region[self.region['ndepth'] == 3]['upward']))


    def get_2depth_region(self):
        depth3_upward = self.region[(self.region['ndepth'] == 3)]['upward']
        region_data = self.region[(self.region['ndepth'] == 3)|((self.region['ndepth'] == 2) & (~self.region['region'].isin(depth3_upward)))]
        region_data.reset_index(drop=True, inplace=True)
        return region_data

    def region_data_modify(self):
        #   충청, 충청남도, 충청북도 데이터 변형
        #   신도시 분당, 양주, 아산 중복 제거
        #   세종 중복 제거
        #   아브뉴프랑, avenuefrance 제거
        #   서울 중구 제거
        self.region.loc[self.region['region'] == '충북', ['synonyms']] = '충북;충청도;충청북도'
        self.region.loc[self.region['region'] == '충남', ['synonyms']] = '충남;충청도;충청남도'

        self.region.loc[self.region['region'] == '상당구', ['synonyms']] = '상당'
        self.region.loc[self.region['region'] == '흥덕구', ['synonyms']] = '흥덕'
        self.region.loc[self.region['region'] == '서원구', ['synonyms']] = '서원'

        for elem in ['청원구', '수정구', '동안구', '음성군', '공주시', '장수군', '완주군', '무주군', '상당구']:
            self.region.loc[self.region['region'] == elem, ['synonyms']] = elem



        self.region.reset_index(drop=True, inplace=True)



    def __delDuplicated(self, l):
        r = []
        for x in l:
            for y in l:
                if x != y and x in y:
                    r.append(y)
        r = list(set(r))
        for z in r:
            l.remove(z)
        return self.__list_to_string(l)


    def __list_to_string(self, l):
        result = ''
        for a in l:
            result += a + ';'
        return result[:-1]


# Quark Data Class
class QuarkDataTable:
    # mimi-PrestoDB
    # required: host, port, schema, username

    def __init__(self, host='media-doraemon-presto01.dakao.io', port=8080, schema='mimi', username='cody.bright'):
        conn = presto.connect(host=host,
                              port=port,
                              schema=schema,
                              username=username)
        query = """
        SELECT distinct e_from as query
        FROM aa.kakao_quark_category 
        where substr(e_to, 1, 12) = '정치/경제/금융_부동산' or substr(e_to, 1, 8) = '지도/지역/교통'
        
        """
        col = ['query']
        cursor = conn.cursor()
        cursor.execute(query)
        self.quark = pd.DataFrame(cursor.fetchall(), columns=col)


class RegionTree:
    def __init__(self, region_data):
        self.element = {}
        self.synonym = {}
        self.scored_elements = []

        for idx, r in region_data.iterrows():
            self.element[r['region']] = RegionTreeElement(r['region'], r['ndepth'])
            for synonym in r['synonyms'].split(';'):
                if synonym in self.synonym:
                    self.synonym[synonym].append(r['region'])
                else:
                    self.synonym[synonym] = [r['region']]

            if r['upward']:
                self.element[r['region']].input_up_element(self.element[r['upward']])
                self.element[r['upward']].input_down_element(self.element[r['region']])


    def reset_elements(self):
        for elem in self.scored_elements:
            elem.score = 0
            elem.on_off = False

    def single_scoring(self, syn):
        for region in self.synonym[syn]:
            if self.element[region] not in self.scored_elements:
                self.scored_elements.append(self.element[region])
            self.element[region].score_up()

    def double_scoring(self, syn, pre_syn):
        for pre_region in self.synonym[pre_syn]:
            for region in self.synonym[syn]:
                if pre_region in [elem.name for elem in self.element[region].upward]:
                    if self.is_connected(region):
                        self.element[region].score_up()
                    else:
                        self.element[region].turn_on_off_true()
                        if self.element[region] not in self.scored_elements:
                            self.scored_elements.append(self.element[region])
                        self.element[region].score_up()
                else:
                    if self.element[region] not in self.scored_elements:
                        self.scored_elements.append(self.element[region])
                    self.element[region].score_up()



    def is_connected(self, region):
        return self.element[region].on_off

    def is_up_region(self, region, pre_region):
        return pre_region in [elem.name for elem in self.element[region].upward]


    def get_best_score_nodes(self):
        best_score_nodes = []
        score = 0
        for elem in self.scored_elements:
            if score < elem.score:
                best_score_nodes = [elem.name]
                score = elem.score
            elif score == elem.score:
                best_score_nodes.append(elem.name)
        return best_score_nodes

    def get_final_best_nodes(self, best_score_nodes, ignore=False):
        xxx = []
        while True:
            xxx = []
            for name in best_score_nodes:
                tmp = self.element[name].get_downward_best_score_nodes(ignore)
                if tmp:
                    xxx += tmp
                else:
                    xxx.append(name)
            if xxx == best_score_nodes:
                break
            else:
                best_score_nodes = xxx
        return xxx


    def get_all_score(self):
        for elem in self.scored_elements:
            print(elem, self.element[elem].score)


""" synonym dict을 통해 점수를 받는다 """
class RegionTreeElement:
    def __init__(self, region, depth):
        self.name = region
        self.upward = []
        self.downward = []
        self.depth = depth
        self.score = 0
        self.on_off = False


    def input_up_element(self, upElement):
        self.upward.append(upElement)
    def input_down_element(self, downElement):
        self.downward.append(downElement)

    def turn_on_off_true(self):
        for elem in self.upward:
            elem.score += self.score
        self.on_off = True

    def score_up(self):
        if self.on_off:
            self.score += 1
            for elem in self.upward:
                elem.score_up()
        else:
            self.score += 1

    def get_downward_best_score_nodes(self, ignore=False):
        score = 0
        best = []
        if ignore:
            for elem in self.downward:
                if elem.on_off:
                    if elem.score > score:
                        best = [elem.name]
                        score = elem.score
                    elif elem.score == score:
                        best.append(elem.name)
        else:
            for elem in self.downward:
                if elem.score > score:
                    best = [elem.name]
                    score = elem.score
                elif elem.score == score:
                    best.append(elem.name)

        if len(best) == 0:
            return None

        return best




def dha_nouns_tokenizer(string):
    dha_dir = '/Users/kakao/Desktop/Workspaces/dha/build'
    dic_dir = '/Users/kakao/Desktop/Workspaces/dha/dha_resources-2.8.92-default'
    dha_obj = dha.DHA(dha_dir)

    coll_name = "default"
    anal_name = "hanl"

    dha_obj.initialize(dic_dir, None, coll_name)

    # DHA 형태소 분석 옵션: 명사만
    options = ["ft_main,-verb_input,-ncp_input,mtag,-dtag,cpos"]

    resultNounsList = ast.literal_eval(dha_obj.analyze(string, anal_name, options)[0])

    return list(map(lambda x: x['str'], resultNounsList))

def check_strings(search_list, input):
    A = ahocorasick.Automaton()
    for idx, s in enumerate(search_list):
        A.add_word(s, (idx, s))
    A.make_automaton()
    output_list = []
    for item in A.iter(input):
        output_list.append([item[0], item[1][1]])
    return output_list

def query_exist_sentences(query, sentences):
    token_query = dha_nouns_tokenizer(query)
    result = ''
    for sentence in divide_sentences(sentences):
        if any(qt in sentence for qt in token_query):
            result += sentence + ' '
    return result[:-1]

def divide_sentences(sentences):
    return re.split("(?<!\S\.\S)(?<=\.|\?)\s", sentences)

def make_brief_region(region):
    if len(region) == 2 or region == '신도시':
        return region
    elif len(region) == 7:
        return region[0:2]
    elif region[-3:] == '신도시':
        return region[:-3]
    else:
        return region[:-1]

def priority_region_detecting(detect_region_names, query, title):
    result = []
    detected = [elem[1] for elem in check_strings(detect_region_names, query)]
    if detected:
        for elem in detected:
            result.append(elem)
    else:
        detected = [elem[1] for elem in check_strings(detect_region_names, title)]
        if detected:
            for elem in detected:
                result.append(elem)
    return result

def remain_most_region(result, sentences):
    most = []
    compare = 0
    for region in result:
        count = sentences.count(region)
        if count < 2:
            pass
        elif count == compare:
            most.append(region)
        elif count > compare:
            most = [region]
            compare = count
    return most

def closed_region_exception(detected_region_result):
    closed = []
    pre = detected_region_result[0]
    for elem in detected_region_result[1:]:
        if elem[0] - pre[0] < 3:
            if len(elem[1]) > len(pre[1]):
                closed.append(pre)
            else:
                closed.append(elem)
        pre = elem
    for elem in closed:
        detected_region_result.remove(elem)
    return detected_region_result




if __name__ == '__main__':
    # 뉴스 데이터 및 검색어 데이터 클래스 정의 및 데이터 테이블 적재
    news_data = NewsDataTable()  # news_data.news: pd.DataFrame, col = 'newsid', 'title', 'sentences'
    query_data = QueryDataTable()  # query_data.query: pd.DataFrame, col = 'query', 'newsid', 'pv'

    # 서로 필터링, pandas merge 이용 (뉴스 - 경제 뉴스/부동산 정규식, 검색어 - 검색을 통해 뉴스를 본 경우)
    news_data.query_filtering(query_data)
    query_data.news_filtering(news_data)

    # 검색어 필터를 위해 쿼크 데이터 테이블 적재 및 필터링
    quark_data = QuarkDataTable()
    query_data.quark_filtering(quark_data.quark)

    # 지역 데이터 테이블 적재 및 검출 지역 리스트 관련 사전 정의
    region_data = RegionDataTable()  # region_data.region: pd.DataFrame, col = 'region', 'ndepth', 'upward', 'synonyms'
    region_data.make_synonym_upward_dict(region_data.region)  # 원래 두 가지 사전을 이용해서 예외처리 하려고 만들었음

    # 일주일 치 데이터 (일주일마다 지역 소비량 랭킹을 뽑고 유입 쿼리를 사전화)
    hot_ranking_region_dict = {}
    region_keyword_dict = {}

    # 지역별 뉴스의 경우 아카이빙 (누적 소비량 일정 이상이 되면 노출한다)
    region_news_dict = {}

    # 아호코라식으로 검출할 지역명 리스트
    detect_region_names = region_data.get_all_synonyms(region_data.region)

    # 지역명 검출 시 점수화를 위한 지역 트리 구조 생성
    region_tree = RegionTree(region_data.region)


    for i, r in query_data.query.iterrows():
        query = r['query']
        newsid = r['newsid']
        title = news_data.get_title(newsid).lower()
        sentences = news_data.get_sentences(newsid).lower()
        # sentences = query_exist_sentences(query, news_data.get_sentences(newsid).lower())
        pv = r['pv']

        final_region_result = []

        # 우선순위가 높은 검색어와 제목에서 지역명 검출
        detected_region_result = priority_region_detecting(detect_region_names, query, title)

        # 본문을 통한 지역 점수 트리에 데이터 저장
        detected_from_sentences = check_strings(detect_region_names, sentences)
        # 본문 검출 결과 지역명이 1개일 경우 바로 점수화
        if len(detected_from_sentences) == 0:
            pass
        elif len(detected_from_sentences) == 1:
            region_tree.single_scoring(detected_from_sentences[0][1])
        else:
            detected_from_sentences = closed_region_exception(detected_from_sentences)
            if len(detected_from_sentences) == 1:
                region_tree.single_scoring(detected_from_sentences[0][1])
            pre = detected_from_sentences[0]
            for elem in detected_from_sentences[1:]:
                if elem[0] - pre[0] < 8:
                    region_tree.double_scoring(elem[1], pre[1])
                else:
                    region_tree.single_scoring(elem[1])
                pre = elem


        if detected_region_result:
            for name in detected_region_result:
                name = region_data.synonym_dict[name]
                final_region_result += region_tree.get_final_best_nodes(name, True)
        else:
            best_nodes = region_tree.get_best_score_nodes()
            final_region_result = region_tree.get_final_best_nodes(best_nodes)

        for area in final_region_result:
            if area in hot_ranking_region_dict:
                hot_ranking_region_dict[area] += pv
                if query in region_keyword_dict[area]:
                    region_keyword_dict[area][query] += pv
                else:
                    region_keyword_dict[area][query] = pv
            else:
                hot_ranking_region_dict[area] = pv
                region_keyword_dict[area] = {}
                region_keyword_dict[area][query] = pv

        region_tree.reset_elements()