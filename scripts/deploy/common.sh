REGION=$(aws configure get region)
AWS_USER_ACCOUNTID=$(aws sts get-caller-identity | python3 -c "import sys, json; print(json.load(sys.stdin)['Account'])")
ROLE="arn:aws:iam::$AWS_USER_ACCOUNTID:role/LambdaRole"
SHARED_LAYER="arn:aws:lambda:${REGION}:$AWS_USER_ACCOUNTID:layer:StoryLayer:6"
S3_LAMBDA_BUCKET="sam-story-analysis"


copyZipToS3BucketFunction(){
  CURRENT_DIRECTORY=$PWD
  cd story-survey-api/${2}
  rm "${CURRENT_DIRECTORY}/upload/${1}.zip"
  aws s3 rm "s3://${S3_LAMBDA_BUCKET}/${1}"
  zip -vr -D "${CURRENT_DIRECTORY}/upload/${1}.zip" .
  aws s3 cp "${CURRENT_DIRECTORY}/upload/${1}.zip" "s3://${S3_LAMBDA_BUCKET}/${1}"
  cd $CURRENT_DIRECTORY
}

updateLambdaFunction(){
    copyZipToS3BucketFunction $1 $2

    aws lambda update-function-code \
    --function-name  $1 \
    --s3-bucket $S3_LAMBDA_BUCKET \
    --s3-key $1
}

# Usage: createLamdaFunction LambdaName FolderName HandlerName
# createLamdaFunction StoryAnalysisLc lc lambda_lc_handler
# createLamdaFunction StoryAnalysisSurvey survey save_handler

createLamdaFunction(){
  copyZipToS3BucketFunction $1 $2

  aws lambda create-function \
    --function-name $1 \
    --runtime python3.8 \
    --code "S3Bucket=${S3_LAMBDA_BUCKET},S3Key=$1" \
    --handler "app.$3" \
    --role "$ROLE" \
    --layers "$SHARED_LAYER" \
    --timeout 900

  aws lambda add-permission --function-name $1 --principal s3.amazonaws.com \
    --statement-id s3invoke --action "lambda:InvokeFunction" \
    --source-arn "arn:aws:s3:::${S3_LAMBDA_BUCKET}" \
    --source-account $AWS_USER_ACCOUNTID
}