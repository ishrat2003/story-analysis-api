aws dynamodb scan \
    --table-name story_survey \
    --query "Items[*].[id.S,created.S]" \
    --endpoint-url http://localhost:8000 --region eu-west-1 \
    --output text