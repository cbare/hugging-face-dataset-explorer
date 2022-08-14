"""
Read dataset info from S3 or local cache.
"""
import json
from pathlib import Path

import boto3
import datasets as ds
from datasets.filesystems import S3FileSystem

from api.search import Index


S3_BUCKET = "jcb-hugging-face-datasets"

dataset_infos_by_name = {}
document_cache = {}
search_indices = {}


def dataset_info_s3(bucket_name=S3_BUCKET):
    """
    Read dataset_info.json files from an S3 bucket. Return a dict keyed by buider_name.
    """
    dataset_infos = {}
    s3 = boto3.resource("s3")
    s3_bucket = s3.Bucket(bucket_name)
    files_in_s3 = [
        f.key for f in
        s3_bucket.objects.all()
        if f.key.endswith("dataset_info.json")
    ]
    for key in files_in_s3:
        f = s3.Object(bucket_name, key)
        dataset_info = json.loads(f.get()["Body"].read().decode("utf-8"))
        dataset_infos[dataset_info["builder_name"]] = dataset_info

    return dataset_infos


def dataset_info_local():
    """
    Read all dataset_info.json files. Return a dict keyed by buider_name.
    """
    dataset_infos = {}
    datasets_root = Path(ds.config.DEFAULT_HF_DATASETS_CACHE)
    for path in datasets_root.glob("**/dataset_info.json"):
        with open(path) as f:
            dataset_info = json.load(f)
            dataset_infos[dataset_info["builder_name"]] = dataset_info

    return dataset_infos


def get_dataset(builder_name, con, split):
    # load encoded_dataset to from s3 bucket
    dataset = ds.load_from_disk(f's3://{S3_BUCKET}/{builder_name}/{con}/',fs=S3FileSystem())
    dataset = dataset[split]
    return dataset


def extract_text_medical_questions_pairs(row):
    return f"{row['question_1']} {row['question_2']}"

def get_docs_and_index(builder_name):
    if builder_name not in indexer_conf:
        raise NotImplementedError(f"Indexer config for {builder_name} not found.")

    if builder_name in search_indices and builder_name in document_cache:
        index = search_indices[builder_name]
        documents = document_cache[builder_name]
    else:
        con, split, extract_text = indexer_conf[builder_name]
        dataset = get_dataset(builder_name, con, split)

        texts = []
        documents = []
        for row in dataset:
            texts.append(extract_text(row))
            documents.append(row)

        index = Index(texts)

        search_indices[builder_name] = index
        document_cache[builder_name] = documents

    return documents, index

def dataset_search(builder_name, q, top=10):
    """
    Search a dataset. Return a list of matching documents.
    """
    if builder_name not in dataset_infos_by_name:
        raise ValueError(f"Dataset {builder_name} not found.")

    documents, index = get_docs_and_index(builder_name)

    indices = index.search(q, top=top)

    con, split, _ = indexer_conf[builder_name]

    return [
        documents[i] for i in indices
    ]


dataset_infos_by_name = dataset_info_s3()

indexer_conf = {
    "medical_questions_pairs": ("default", "train", extract_text_medical_questions_pairs)
}
