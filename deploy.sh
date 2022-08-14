set -e
set -x

# build
docker build --tag hugging-face-dataset-explorer:latest .

# tag with upstream repo
docker tag hugging-face-dataset-explorer:latest 017619365500.dkr.ecr.us-west-2.amazonaws.com/hugging-face-dataset-explorer:latest

# push to ECR
docker push 017619365500.dkr.ecr.us-west-2.amazonaws.com/hugging-face-dataset-explorer:latest

# deploy to lambda
aws lambda update-function-code --function-name hugging-face-dataset-explorer --image-uri 017619365500.dkr.ecr.us-west-2.amazonaws.com/hugging-face-dataset-explorer:latest
