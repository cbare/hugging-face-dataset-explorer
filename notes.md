# Project notes for Hugging Face demo

- create venv
- create README and .gitignore
- git init and initial commit
- create bucket jcb-hugging-face-datasets
- upload datasets

```sh
aws s3 cp ~/.cache/huggingface/datasets/ s3://jcb-hugging-face-datasets/ --recursive --exclude "*.lock" --exclude "downloads/*"
```

- create IAM user hf-dataset-explorer and group hf-dataset-explorer-grp
- create [access policy][1] for group to access bucket
- [upgrade aws cli][2] from 2.7.19 to 2.7.22

```sh
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

- create bucket for code: jcb-hugging-face-datasets-code

```sh
aws s3 cp lambda_function.zip s3://jcb-hugging-face-datasets-code/
```

- install CDK 2.37.1 (build f15dee0) - [CDK Getting started][3]

```sh
npm install -g aws-cdk
cdk --version
```

- verify aws IAM user

```sh
aws sts get-caller-identity --profile hf-dataset-explorer
aws configure get region --profile hf-dataset-explorer
```

This needed super-dooper permissions. Not sure I want to go down this route.

```sh
cdk bootstrap aws://017619365500/us-west-2
```

## Docker

- build Dockerfile

```sh
docker build --tag hugging-face-dataset-explorer:latest .
```

The container has some lambda scaffolding built into it that expects input in a special payload format. It would be nice to figure out how to invoke it locally like the lambda machinery will. To run in docker:

```sh
docker run --rm -v /Users/jchristopherbare/.aws:/root/.aws -p 8000:8080 hugging-face-dataset-explorer:latest
```

To work with the nice api we've defined in FastAPI, we can run with uvicorn by overriding the lambda entrypoint:

```sh
docker run --rm -d -p 8000:8000 -v /Users/jchristopherbare/.aws:/root/.aws --entrypoint uvicorn hugging-face-dataset-explorer:latest "api.main:app" "--host" "0.0.0.0" "--port" "8000"
```

## Push container to ECR

- in ECR create repo: hugging-face-dataset-explorer

```sh
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 017619365500.dkr.ecr.us-west-2.amazonaws.com
```

```sh
docker build --tag hugging-face-dataset-explorer:latest .

docker tag hugging-face-dataset-explorer:latest 017619365500.dkr.ecr.us-west-2.amazonaws.com/hugging-face-dataset-explorer:latest

docker push 017619365500.dkr.ecr.us-west-2.amazonaws.com/hugging-face-dataset-explorer:latest
```

## Lambda

- deploy docker container image into lambda, see: `deploy.sh`
- add bucket policy to lambda execution role
- in lambda console, [create test event using apigateway-aws-proxy template][4], setting path (3 places) and method (2 places)
- test in lambda console
- turn on function url, wide open to start, and test endpoint

```sh
http https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws/
```


[1]: data/bucket-policy.json
[2]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
[3]: https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html
[4]: https://www.youtube.com/watch?v=RGIM4JfsSk0
