# zip , s3 upload, aws lambda commandline update
rm aifblambda.zip
zip aifblambda.zip -r data/ dynamoKB.py jieba/ lambda_ai.py socialBrain.py basickb.csv requests/  pttChat.py basickb.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials esHealth.py esBible.py awsconfig
aws s3 cp aifblambda.zip s3://sandyai2/
aws lambda update-function-code --function-name fbaipost --s3-bucket sandyai2 --s3-key aifblambda.zip
