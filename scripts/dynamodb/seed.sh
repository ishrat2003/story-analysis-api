#!/bin/bash
source "$PWD/scripts/dynamodb/common.sh"

cmd="aws dynamodb $endPoint --region $region create-table --cli-input-json file://$PWD/database/dynamodb/seed/$tableName.json"
eval $cmd

cmd="aws dynamodb $endPoint --region $region create-table --cli-input-json file://$PWD/database/dynamodb/seed/rcstoryreview.json"
eval $cmd