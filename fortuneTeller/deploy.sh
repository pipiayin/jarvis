# To deploy lambda on AWS
rm lottery.zip
zip lottery.zip -r lambda_lottery.py lottery60.py
#aws --profile ailine s3 cp taipeibus.html s3://taipeibus/
aws --profile ailine s3 cp lottery.zip s3://sandyai2/
#aws --profile ailine lambda create-function --function-name lottery --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_lottery.lambda_handler --timeout 10 --code "S3Bucket=sandyai2,S3Key=lottery.zip"

aws --profile ailine lambda update-function-code --function-name lottery --s3-bucket sandyai2 --s3-key lottery.zip



