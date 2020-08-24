REGION=$(aws configure get region)

aws dynamodb list-tables --endpoint-url http://localhost:8000 --region eu-west-1

