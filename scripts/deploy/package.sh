sam build --template-file ./story-survey-api/template.yaml

sam package \
  --template-file ./story-survey-api/template.yaml \
  --output-template-file ./story-survey-api/package.yml \
  --s3-bucket sam-story-analysis