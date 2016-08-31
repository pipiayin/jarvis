# zip , s3 upload, aws lambda commandline update
rm ailambda.zip
zip ailambda.zip -r data/ dynamoKB.py jieba/ lambda_ai.py socialBrain.py basickb.csv requests/  pttChat.py basickb.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials
aws s3 cp ailambda.zip s3://sandyai/
aws lambda update-function-code --function-name sandyaipost --s3-bucket sandyai --s3-key ailambda.zip
