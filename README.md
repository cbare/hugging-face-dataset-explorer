# Dataset Explorer

Demo querying the dataset [medical_questions_pairs][1], a semantic similarity dataset consisting of 3048 similar and dissimilar medical question pairs hand-generated and labeled by Curai's doctors.

## Getting started

This project exposes a REST API for querying dataset metadata and text search on the individual documents. I'm interested in healthcare applications, so I found a set of medical questions.

There are 4 endpoints, each demonstrated below using [httpie][3]:

### Top level welcome message and info

```sh
http "https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws"
```

### List available datasets

```sh
http "https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws/datasets"
```

### Show dataset info for a single dataset

```sh
http "https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws/dataset/medical_questions_pairs"
```

### Search within dataset documents

Search for dataset documents matching keywords in the query string.

```sh
http "https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws/search/medical_questions_pairs?q=lisinopril"
```

```sh
http "https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws/search/medical_questions_pairs?q=hazardous"
```

### Note on latency

The API is deployed on AWS Lambda and is therefore subject to coldstart latency. I load dataset metadata when the app loads and build a tfidf search index when first queried which is probably not an ideal fit for Lambda, were it not for my natural cheapness. A higher performace tier or provisioned capacity would be enough to overcome this issue, but doing the indexing in a dedicated service would be preferred for a non-toy project.

The API may time out on first access, but it fairly snappy after that.

### Tools

- Hugging Face datasets
- Docker
- FastAPI
- scikit-learn
- spacy
- AWS Lambda
- S3


## Development

To run the api:

```sh
uvicorn api.main:app --reload
```

```sh
http http://127.0.0.1:8000
```

We also get nice [API docs][2].

### Tests

To run tests:

```sh
PYTHONPATH=. pytest -v --cov=api tests/
```

### Docker

To build the docker image:

```sh
docker build --tag hugging-face-dataset-explorer:latest .
```

We'll deploy a Docker container to AWS lambda, so we have to push our container image to an AWS container repo (ECR). First authenticate with ECR if necessary:

```sh
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 017619365500.dkr.ecr.us-west-2.amazonaws.com
```

Build the docker container image and push:

```sh
./deploy.sh
```

[1]: https://huggingface.co/datasets/medical_questions_pairs
[2]: https://wi4cfo42pfyjgalamfvtr7bwwe0kzdjt.lambda-url.us-west-2.on.aws/docs
[3]: https://httpie.io/
