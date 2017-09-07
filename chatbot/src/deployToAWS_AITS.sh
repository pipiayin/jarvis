# zip , s3 upload, aws lambda commandline update
rm ailine.zip
rm aiBrain.zip
rm aiLearn.zip
rm lineResponse.zip
rm linegenbot.zip


zip aiBrain.zip -r data/ jieba/ lambda_brain.py socialBrain.py basickb.csv requests/  pttChat.py basickb.csv wikiChat.py esKB.py elasticsearch/ urllib3 requests_aws4auth/ credentials esHealth.py esBible.py linecre.so awsconfig.py credentials_ai nocheckin.py genericKB.py blackList.py lineTools.py config.py twMessageProcess.py lambda_simplekb.py aiConfig.py aiProfile.py
zip aiLearn.zip -r  elasticsearch/ urllib3 requests/ requests_aws4auth/ credentials linecre.so awsconfig.py credentials_ai nocheckin.py lambda_learn.py genericKB.py blackList.py lineTools.py
zip ailine.zip -r lambda_line.py nocheckin.py requests/ urllib3 genericKB.py lineTools.py blackList.py config.py 
zip lineResponse.zip -r lambda_lineResponse.py nocheckin.py requests/ lineTools.py

aws --profile ailine s3 cp aiBrain.zip s3://sandyai2/
aws --profile ailine s3 cp ailine.zip s3://sandyai2/
aws --profile ailine s3 cp aiLearn.zip s3://sandyai2/
aws --profile ailine s3 cp lineResponse.zip s3://sandyai2/

aws --profile ailine lambda update-function-code --function-name linepost --s3-bucket sandyai2 --s3-key ailine.zip
aws --profile ailine lambda update-function-code --function-name aibrain --s3-bucket sandyai2 --s3-key aiBrain.zip
aws --profile ailine lambda update-function-code --function-name ailearn --s3-bucket sandyai2 --s3-key aiLearn.zip
aws --profile ailine lambda update-function-code --function-name lineResponse --s3-bucket sandyai2 --s3-key lineResponse.zip
