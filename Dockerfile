FROM amazon/aws-lambda-python:3.9

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY api ${LAMBDA_TASK_ROOT}/api

CMD ["api.main.handler"]
