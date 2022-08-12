from pathlib import Path
import json


def index_datasets():
    """
    Read all dataset_info.json files.
    """
    datasets = {}
    datasets_root = Path("./datasets")
    for path in datasets_root.glob("**/dataset_info.json"):
        with open(path) as f:
            dataset_info = json.load(f)
            datasets[dataset_info["builder_name"]] = dataset_info

    return datasets

datasets = index_datasets()
