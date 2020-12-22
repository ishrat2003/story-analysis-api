#!/bin/bash
source "$PWD/scripts/dynamodb/common.sh"

cmd="aws dynamodb $endPoint --region $region scan --table-name $tableName --query \"Items[*].[user_code.S,story_link.S]\" --output text"
echo $cmd
eval $cmd