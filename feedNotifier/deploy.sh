# To deploy lambda on AWS
rm weatherNotify.zip
rm dailyenglishNotify.zip
rm myth.zip
zip weatherNotify.zip -r lambda_weathernotify.py feedparser.py weatherFeed.py
zip myth.zip -r lambda_myth.py feedparser.py mythBusters.py
zip dailyenglishNotify.zip -r feedparser.py lambda_dailyenglish.py dailyEnglishFeed.py
#aws --profile ailine s3 cp taipeibus.html s3://taipeibus/
aws --profile ailine s3 cp weatherNotify.zip s3://sandyai2/
aws --profile ailine s3 cp dailyenglishNotify.zip s3://sandyai2/
aws --profile ailine s3 cp myth.zip s3://sandyai2/
#aws --profile ailine lambda create-function --function-name weathernotify --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_weathernotify.lambda_handler --timeout 10 --code "S3Bucket=sandyai2,S3Key=weatherNotify.zip"
#aws --profile ailine lambda create-function --function-name dailyenglishnotify --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_dailyenglish.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=dailyenglishNotify.zip"
aws --profile ailine lambda create-function --function-name myth --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_myth.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=myth.zip"

aws --profile ailine lambda update-function-code --function-name weathernotify --s3-bucket sandyai2 --s3-key weatherNotify.zip
aws --profile ailine lambda update-function-code --function-name dailyenglishnotify --s3-bucket sandyai2 --s3-key dailyenglishNotify.zip
aws --profile ailine lambda update-function-code --function-name myth --s3-bucket sandyai2 --s3-key myth.zip



