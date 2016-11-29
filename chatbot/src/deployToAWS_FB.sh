# zip , s3 upload, aws lambda commandline update
rm aifblambda.zip
rm aifbresponse.zip
zip aifblambda.zip lambda_fb.py 
zip aifbresponse.zip -r data/ dynamoKB.py  socialBrain.py basickb.csv requests/  pttChat.py basickb.csv basickb_en.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials esHealth.py esBible.py awsconfig.py nocheckin.py linecre.so awsconfig.py credentials_ai nocheckin.py genericKB.py lambda_fbresponse.py  nltk_data socialEnBrain.py  wikiFinder.py
aws s3 cp aifblambda.zip s3://sandyai2/
aws s3 cp aifbresponse.zip s3://sandyai2/
aws lambda update-function-code --function-name fbaipost --s3-bucket sandyai2 --s3-key aifblambda.zip
aws lambda update-function-code --function-name fbresponse --s3-bucket sandyai2 --s3-key aifbresponse.zip
