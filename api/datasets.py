from pathlib import Path
import json

import sys
for path in sys.path:
    print(path)

import datasets as ds


datasets_by_name = {}


def index_datasets():
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

def preview_dataset(builder_name):
    dataset_info = datasets_by_name[builder_name]


datasets_by_name = index_datasets()
