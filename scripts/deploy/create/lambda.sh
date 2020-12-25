#!/bin/bash
source "$PWD/scripts/deploy/common.sh"

# Usage: createLamdaFunction LambdaName FolderName HandlerName
createLamdaFunction story_analysis_lc lc lambda_lc_handler
createLamdaFunction story_analysis_survey survey save_handler
aws apigateway create-deployment --rest-api-id story-analysis-api --region $REGION
