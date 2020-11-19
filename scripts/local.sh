echo "Starting local environment"
echo -e "----------------------------\n"
NETWORK_NAME='sam-net-story-survey-api'
DB_CONTAINER_NAME='sam-db-story-survey-api'
LOCAL_DB_PATH='./database/dynamodb'

pip3 install -U nltk
python3 -m nltk.downloader punkt -d ./story-survey-api/nltk
python3 -m nltk.downloader averaged_perceptron_tagger -d ./story-survey-api/nltk
python3 -m nltk.downloader stopwords -d ./story-survey-api/nltk

echo "\n1. Network"
echo -e "----------------------------\n"

echo "Deleting $NETWORK_NAME"
docker network rm "$NETWORK_NAME"

echo "Creating $NETWORK_NAME"
docker network create -d bridge "$NETWORK_NAME"


echo -e "\n2. Dynamodb"
echo -e "----------------------------\n"

echo "Stopping dynamodb container $DB_CONTAINER_NAME"
docker rm "$DB_CONTAINER_NAME"

echo "Starting dynamodb container $DB_CONTAINER_NAME"
docker run -d -v "$PWD$LOCAL_DB_PATH:/data" -p 8000:8000 --network "$NETWORK_NAME" --name "$DB_CONTAINER_NAME" amazon/dynamodb-local 

echo -e "\n3. Starting application"
echo -e "----------------------------\n"

echo "Validating Cloud Formation template"
sam validate --template-file ./story-survey-api/template.yaml 

echo "Starting"
sam local start-api  --template-file ./story-survey-api/template.yaml  --env-vars env.json --port 3500

echo -e "----------------------------\n"
echo "Finished"
