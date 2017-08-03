# To deploy lambda on AWS
rm pixnet.zip

zip pixnet.zip -r lambda_pixnet.py  pixnetTool.py  requests/  twlocation.py

aws --profile ailine s3 cp pixnet.zip s3://sandyai2/

#aws --profile ailine lambda create-function --function-name pixnetfood --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_pixnet.lambda_foodhandler --timeout 59 --code "S3Bucket=sandyai2,S3Key=pixnet.zip"
#aws --profile ailine lambda create-function --function-name pixnetfans --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_pixnet.lambda_fanshandler --timeout 59 --code "S3Bucket=sandyai2,S3Key=pixnet.zip"

aws --profile ailine lambda update-function-code --function-name pixnetfood --s3-bucket sandyai2 --s3-key pixnet.zip
aws --profile ailine lambda update-function-code --function-name pixnetfans --s3-bucket sandyai2 --s3-key pixnet.zip



