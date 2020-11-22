aws dynamodb scan \
    --table-name story_survey \
    --query "Items[*].[user_code.S,story_link.S]" \
    --endpoint-url http://localhost:8000 --region eu-west-1 \
    --output text