import json
from pathlib import Path

import boto3
import datasets as ds


S3_BUCKET = "jcb-hugging-face-datasets"

datasets_by_name = {}


def index_datasets_s3():
    datasets = {}
    s3 = boto3.resource("s3")
    s3_bucket = s3.Bucket(S3_BUCKET)
    files_in_s3 = [
        f.key for f in
        s3_bucket.objects.all()
        if f.key.endswith("dataset_info.json")
    ]
    for file_name in files_in_s3:
        f = s3.Object(S3_BUCKET, file_name)
        dataset_info = json.loads(f.get()["Body"].read().decode("utf-8"))
        datasets[dataset_info["builder_name"]] = dataset_info

    return datasets


def index_datasets_local():
    """
    Read all dataset_info.json files. Return a dict keyed by buider_name.
    """
    datasets = {}
    datasets_root = Path(ds.config.DEFAULT_HF_DATASETS_CACHE)
    for path in datasets_root.glob("**/dataset_info.json"):
        with open(path) as f:
            dataset_info = json.load(f)
            datasets[dataset_info["builder_name"]] = dataset_info

    return datasets


datasets_by_name = index_datasets_s3()
