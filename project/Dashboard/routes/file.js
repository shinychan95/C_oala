const express = require('express');
const router = express.Router();
const { spawn } = require('child_process')
const fs = require('fs');
const multer = require('multer');
const storage = multer.diskStorage({
    destination(req, file, callback) {
        callback(null, 'uploads');
    },
    filename(req, file, callback) {
        let array = file.originalname.split('.');
        array[0] = array[0] + '_';
        array[1] = '.' + array[1];
        array.splice(1, 0, Date.now().toString());
        const result = array.join('');
        console.log(result);
        callback(null, result);
    }
});
const upload = multer({
    storage,
    limits: {
        files: 10,
        fileSize: 1024 * 1024 * 1024,
    }
});



const rmdirAsync = function(path, callback) {
	fs.readdir(path, function(err, files) {
		if(err) {
			// Pass the error on to callback
			callback(err, []);
			return;
		}
		var wait = files.length,
			count = 0,
			folderDone = function(err) {
            count++;
            if( count >= wait || err) {
                fs.mkdir(path,callback);
            }
			// If we cleaned out all the files, continue
			// if( count >= wait || err) {
			// 	fs.rmdir(path,callback);
			// }
		};
		// Empty directory to bail early
		if(!wait) {
			folderDone();
			return;
		}
		
		// Remove one or more trailing slash to keep from doubling up
		path = path.replace(/\/+$/,"");
		files.forEach(function(file) {
			var curPath = path + "/" + file;
			fs.lstat(curPath, function(err, stats) {
				if( err ) {
					callback(err, []);
					return;
				}
				if( stats.isDirectory() ) {
					rmdirAsync(curPath, folderDone);
				} else {
					fs.unlink(curPath, folderDone);
				}
			});
		});
	});
};




router.post('/upload', upload.array('photo', 1), function(req, res, next) {
    try {
        const files = req.files;
        let originalName = '';
        let fileName = '';
        let mimeType = '';
        let size = 0;

        if (Array.isArray(files)) {
            console.log(`files is array~`);
            originalName = files[0].originalname;
            fileName = files[0].filename;
            mimeType = files[0].mimetype;
            size = files[0].size;
        } else {
            console.log(`files is not array~`);
            originalName = files[0].originalname;
            fileName = files[0].filename;
            mimeType = files[0].mimetype;
            size = files[0].size;
        }
        console.log(`file inform : ${originalName}, ${fileName}, ${mimeType}, ${size}`);
        
        res.redirect('/files/builds');
    
    } catch (err) {
        console.dir(err.stack);
    }
});

router.get('/builds', saveInDatabase)

function saveInDatabase(req, res) {
    let name = ''
    console.log('Now we have a http message with headers but no data yet.');
    req.on('data', chunk => {
        console.log('A chunk of data has arrived: ', chunk);
        name += JSON.parse(chunk).username;
    });
    req.on('end', () => {
        console.log('No more data');
        const Save = spawn('python',['C:\\github\\C_oala\\project\\data\\data_processing.py']); 
        
        Save.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        
        Save.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        
        Save.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
            rmdirAsync(`C:\\github\\C_oala\\project\\dashboard-nodejs\\uploads`, () => {
                res.redirect('/');
            }) 
        })    
    });
};
  


module.exports = router;