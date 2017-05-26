# zip , s3 upload, aws lambda commandline update
#zip aiBrain.zip -r data/ jieba/ lambda_brain.py socialBrain.py basickb.csv requests/  pttChat.py basickb.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials esHealth.py esBible.py linecre.so awsconfig.py credentials_ai nocheckin.py genericKB.py blackList.py
#zip aiLearn.zip -r  elasticsearch/ urllib3 requests/ requests_aws4auth/ credentials linecre.so awsconfig.py credentials_ai nocheckin.py lambda_learn.py genericKB.py blackList.py
aws --profile ailine s3 cp taipeibus.html s3://taipeibus/
aws --profile ailine s3 cp all.js s3://taipeibus/
#aws --profile ailine lambda update-function-code --function-name linepost --s3-bucket sandyai2 --s3-key ailine.zip
