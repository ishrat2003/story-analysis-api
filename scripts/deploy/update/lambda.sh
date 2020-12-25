#!/bin/bash
source "$PWD/scripts/deploy/common.sh"

# Usage: updateLambdaFunction LambdaName FolderName
updateLambdaFunction story_analysis_lc lc
updateLambdaFunction story_analysis_survey survey