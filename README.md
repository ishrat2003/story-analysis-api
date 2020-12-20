# Story survey api

https://itnext.io/creating-aws-lambda-applications-with-sam-dd13258c16dd

https://github.com/heitorlessa/sam-local-python-hot-reloading

import nltk
import json
from nltk.tokenize import word_tokenize

nltk.data.path.append("/tmp")

nltk.download("punkt", download_dir = "/tmp")


https://medium.com/@gurlgilt/deploying-aws-sam-lambda-api-gateway-dynamodb-and-s3-ad11e619d322

https://github.com/ganshan/sam-dynamodb-local


To validate sam template use 

sam validate -t story-survey-api/template.yaml 


Description of the table

aws sam-db-story-survey-api describe-table --table-name=story_survey

Execute seed

aws sam-db-story-survey-api create-table --cli-input-json /database/dynamodb/seed/story_survey.json

===

docker build -t aws-lambda-python-latest:latest .