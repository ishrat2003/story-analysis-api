#!/bin/bash
source "$PWD/scripts/deploy/common.sh"

# # Update Lambdas
# updateLambdaFunction story_analysis_lc lc
# updateLambdaFunction story_analysis_survey survey

# Build sam template
sam build --template-file ./story-survey-api/production-template.yaml

# # Build sam package
sam package \
  --template-file ./story-survey-api/production-template.yaml \
  --output-template-file ./story-survey-api/production-package.yaml \
  --s3-bucket sam-story-analysis

# Execute sam deploy
sam deploy \
  --template-file ./story-survey-api/production-package.yaml \
  --stack-name story-analysis \
  --capabilities CAPABILITY_IAM \
  --region $REGION \
  --s3-bucket $S3_LAMBDA_BUCKET \
  --guided

