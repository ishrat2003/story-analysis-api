aws dynamodb scan \
    --table-name localStoryReview \
    --query "Items[*].[user_code.S,story_link.S]" \
    --endpoint-url http://localhost:8000 --region eu-west-1 \
    --output text