#!/bin/bash
source "$PWD/scripts/dynamodb/common.sh"

cmd="aws dynamodb $endPoint --region $region list-tables"
eval $cmd