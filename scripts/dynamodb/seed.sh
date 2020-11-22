LOCAL_DB_PATH='./database/dynamodb'

# 
# aws dynamodb --endpoint-url http://localhost:8000 --region eu-west-1 delete-table --table-name story_survey

aws dynamodb --endpoint-url http://localhost:8000 --region eu-west-1 create-table --cli-input-json file:///Users/ishratsami/Workspace/backend-frontend/Research/MyProjects/story-survey-api/database/dynamodb/seed/story_survey.json