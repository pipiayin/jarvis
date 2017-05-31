# To deploy lambda on AWS
rm lottery.zip
rm astro.zip
rm dayfortune.zip
zip lottery.zip -r lambda_lottery.py lottery60.py
zip astro.zip -r lambda_astro.py astroTool.py requests/ hanziconv/
zip dayfortune.zip -r lambda_dayfortune.py dayFortuneTool.py  requests/ hanziconv/
#aws --profile ailine s3 cp taipeibus.html s3://taipeibus/
aws --profile ailine s3 cp lottery.zip s3://sandyai2/
aws --profile ailine s3 cp astro.zip s3://sandyai2/
aws --profile ailine s3 cp dayfortune.zip s3://sandyai2/
#aws --profile ailine lambda create-function --function-name lottery --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_lottery.lambda_handler --timeout 10 --code "S3Bucket=sandyai2,S3Key=lottery.zip"
#aws --profile ailine lambda create-function --function-name astro --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_astro.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=astro.zip"
aws --profile ailine lambda create-function --function-name dayfortune --runtime python3.6 --role "arn:aws:iam::740157263594:role/sandyairun" --handler lambda_dayfortune.lambda_handler --timeout 59 --code "S3Bucket=sandyai2,S3Key=dayfortune.zip"

aws --profile ailine lambda update-function-code --function-name lottery --s3-bucket sandyai2 --s3-key lottery.zip
aws --profile ailine lambda update-function-code --function-name astro --s3-bucket sandyai2 --s3-key astro.zip
aws --profile ailine lambda update-function-code --function-name dayfortune --s3-bucket sandyai2 --s3-key dayfortune.zip



