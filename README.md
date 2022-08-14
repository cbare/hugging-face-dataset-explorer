# Medical question pairs

Demo using the dataset [medical_questions_pairs][1], a semantic similarity dataset consisting of 3048 similar and dissimilar medical question pairs hand-generated and labeled by Curai's doctors.


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

We'll deploy a Docker container to AWS lambda, so we have to push our container image to an AWS container repo (ECR):

```sh
./deploy.sh
```

[1]: https://huggingface.co/datasets/medical_questions_pairs
[2]: http://127.0.0.1:8000/docs
