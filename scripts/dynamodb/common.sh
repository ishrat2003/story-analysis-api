#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -e environmentName"
   echo -e "\t-e: environmentName ex: prod|local"
   echo "Ex: ./scripts/dynamodb/remove.sh -e local"
   exit 1 # Exit script after printing help
}

while getopts "e:" opt
do
   case "$opt" in
      e ) environmentName="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Begin script in case all parameters are correct
echo "Environment Name: $environmentName"

# Print helpFunction in case parameters are empty
if [ -z "$environmentName" ];
then
   echo "Some or all of the parameters are empty"
   helpFunction
fi

endPoint=""
if test $environmentName = "local";
then
   endPoint=" --endpoint-url http://localhost:8000"
fi

tableName="localstoryreview"
region=$(aws configure get region)