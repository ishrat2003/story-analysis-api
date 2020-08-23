Create a S3 bucket for storing SAM deployment artifacts in the us-east-1 region (or a region of your choosing). Please note that you may not use '-' or '.' in your bucket name.
aws s3 mb s3://{s3-bucket-name} --region us-east-1

Create the Serverless Application Model package using CLI.
sam package \
--region us-east-1 \
--template-file template.yml \
--s3-bucket {s3-bucket-name} \
--output-template-file packaged.yml

Deploy the packaged template.
aws cloudformation deploy \
--region us-east-1 \
--template-file packaged.yml \
--stack-name {stack_name} \
--capabilities CAPABILITY_IAM

After the stack has been successfully created, you may test the application using the CURL commands as shown above.

when you run sam local start-api --env-vars env.json and it will print 123

p.s. it will work with start-api/start-lambda/invoke all in the same way, but it looks like sam deploy only works with --parameter-overrides SomeVar=other_value and no --env-vars

share  