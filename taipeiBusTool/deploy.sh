# zip , s3 upload, aws lambda commandline update
#zip aiBrain.zip -r data/ jieba/ lambda_brain.py socialBrain.py basickb.csv requests/  pttChat.py basickb.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials esHealth.py esBible.py linecre.so awsconfig.py credentials_ai nocheckin.py genericKB.py blackList.py
rm taipeibus.zip
zip taipeibus.zip -r requests/ lambda_bus.py rtBus.py
#aws --profile ailine s3 cp taipeibus.html s3://taipeibus/
aws --profile ailine s3 cp taipeibus.zip s3://sandyai2/
aws --profile ailine lambda update-function-code --function-name taipeibus --s3-bucket sandyai2 --s3-key taipeibus.zip
