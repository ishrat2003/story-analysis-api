#!/bin/bash
source "$PWD/scripts/dynamodb/common.sh"

cmd="aws dynamodb $endPoint --region $region delete-table --table-name $tableName"
eval $cmd
