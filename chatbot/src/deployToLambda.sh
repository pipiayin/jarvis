# zip , s3 upload, aws lambda commandline update
zip ailambda.zip -r data/ dynamoKB.py jieba/ lambda_ai.py socialBrain.py basickb.csv requests/ requests-2.11.1.dist-info/ pttChat.py basickb.csv
aws s3 cp ailambda.zip s3://test-tschen/
aws lambda update-function-code --function-name answer --s3-bucket test-tschen --s3-key ailambda.zip
