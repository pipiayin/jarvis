# To deploy lambda on AWS
rm weatherNotify.zip
zip weatherNotify.zip -r lambda_weathernotify.py feedparser.py weatherFeed.py
#aws --profile ailine s3 cp taipeibus.html s3://taipeibus/
aws --profile ailine s3 cp weatherNotify.zip s3://sandyai2/
aws --profile ailine lambda create-function --function-name weathernotify --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_weathernotify.lambda_handler --timeout 10 --code "S3Bucket=sandyai2,S3Key=weatherNotify.zip"
#aws --profile ailine lambda create-function --function-name dayfortune --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_dayfortune.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=dayfortune.zip"

aws --profile ailine lambda update-function-code --function-name weathernotify --s3-bucket sandyai2 --s3-key weatherNotify.zip



