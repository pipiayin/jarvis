# zip , s3 upload, aws lambda commandline update
rm ailine.zip
rm aiBrain.zip
zip aiBrain.zip -r data/ dynamoKB.py jieba/ lambda_ai.py socialBrain.py basickb.csv requests/  pttChat.py basickb.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials esHealth.py esBible.py
zip ailine.zip -r lambda_line.py
aws --profile ailine s3 cp aiBrain.zip s3://sandyai2/
aws --profile ailine s3 cp ailine.zip s3://sandyai2/
aws --profile ailine lambda update-function-code --function-name linepost --s3-bucket sandyai2 --s3-key ailine.zip
aws --profile ailine lambda update-function-code --function-name aibrain --s3-bucket sandyai2 --s3-key aiBrain.zip
