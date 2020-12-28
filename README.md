# Story Analysis Api

Story analysis is an academic project sponsored by <b><a href="https://www.gold.ac.uk/">Goldsmiths, University of London</a></b> and <b><a href="https://www.thebyte9.com/">Byte9, London</a></b>. Written documents not only contains topic related information for NLP tasks but also preserves the writer’s rhetoric and cognitive connectivity of the underlying concepts and actions. Inspired by <b><a href="https://en.wikipedia.org/wiki/Hero%27s_journey">Joseph Campbell’s "The Hero’s Journey"</a></b>, this API extracts terms from document for evaluating the cognitive richness of the underlying extraction. It also uses <b><a href="https://developers.google.com/knowledge-graph">Google’s Knowledge Graph API</a></b> for categorization.</p>

## Setup Instructions

1. Setup Docker and AWS CLI locally with IAM user with the required permissions.
2. Setup dependent lambda layer. Setup [story-analysis-layers](https://github.com/ishrat2003/story-analysis-layers) project localy and run the following script inside the project to upload required packages. 
    ```sh
    $ cd story-analysis-layers
    $ ./scripts/install.sh -p 3.8 -u yes -l StoryLayer
    ```
2. Run the following script to setup dynamodb in AWS.
    ```sh
    $ ./scripts/dynamodb/seed.sh -e production
    ```

3. Setup S3 bucket in AWS. We have created a bucket name "sam-story-analysis". Update S3_LAMBDA_BUCKET and other necessary script variables in /scripts/deploy/common.sh. Execute the following script to create lambda functions for LC and Survey.
    ```sh
    $ ./scripts/deploy/create/lambda.sh
    ```
    After creation to update lambda run the following script.
    ```sh
    $ ./scripts/deploy/update/lambda.sh
    ```
4. Setup the following environment variables for the LC lambda.
    ```sh
    ENVIRONMENT_NAME: "production"
    GOOGLE_KNOWLEDGE_GRAPH: "YOUR_GOOGLE_KNOWLEDGE_GRAPH_KEY"
    ```
5. Setup the following environment variables for the Survey lambda.
    ```sh
    ENVIRONMENT_NAME: "production"
    DYNAMODB_ENDPOINT: "https://dynamodb.eu-west-1.amazonaws.com"
    DEFAULT_DYNAMODB_ENDPOINT: "http://host.docker.internal:8000"
    TABLE_NAME: "localstoryreview"
    ```
6. Setup API Gateway and endpoints for LC and Survey in AWS admin.
<div style='float: center'>
  <img style='width: 500px' src="./docs/images/api-gateway-2.png"></img>
</div>
<div style='float: center'>
  <img style='width: 500px' src="./docs/images/api-gateway-3.png"></img>
</div>
<div style='float: center'>
  <img style='width: 500px' src="./docs/images/api-gateway-1.png"></img>
</div>

7. To test using [Postman](https://www.postman.com/). Import the collection from [here](./docs/api.postman_collection.json). Add the following postman environment variables.
    ```sh
    API_URL http://127.0.0.1:3500
    GOOGLE_KNOWLEDGE_GRAPH "YOUR_GOOGLE_KNOWLEDGE_GRAPH_KEY"
    ```

## Setup local API

1. Copy story-survey-api/production-template.yaml to story-survey-api/template.yaml
2. Execute the following command to start local server.
    ```sh
    $ ./scripts/local/start.sh
    ```
3. Setup local DynamoDb table using the following script.
    ```sh
    $ ./scripts/dynamodb/seed.sh -e local
    ```
4. Execute the following command to start local server.
    ```sh
    $ ./scripts/local/terminate.sh
    ```

## Note

If you use this code please reference the relevant [publication(s)](http://ishratsami.blogspot.com/p/publications.html).