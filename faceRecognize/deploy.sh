# To deploy lambda on AWS
rm facerecognize.zip

zip facerecognize.zip -r lambda_facerecognize.py  requests/ nocheckin.py wikiFinder.py boto3/ botocore/ lineTools.py

aws --profile ailine s3 cp facerecognize.zip s3://sandyai2/

#aws --profile ailine lambda create-function --function-name facerecognize --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_facerecognize.lambda_handler --timeout 120 --code "S3Bucket=sandyai2,S3Key=facerecognize.zip"
#aws --profile ailine lambda create-function --function-name astro --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_astro.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=astro.zip"
#aws --profile ailine lambda create-function --function-name dayfortune --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_dayfortune.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=dayfortune.zip"

aws --profile ailine lambda update-function-code --function-name facerecognize --s3-bucket sandyai2 --s3-key facerecognize.zip



