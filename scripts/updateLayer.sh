docker build -t aws-lambda-python-latest:latest .

docker run aws-lambda-python-latest -p 9000:8080   -d -v story-survey-api/layers:/home/layers

