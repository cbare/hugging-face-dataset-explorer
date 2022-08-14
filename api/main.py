"""
Entry point for the API.
"""
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from api.__version__ import __version__
from api.datasets import dataset_infos_by_name, dataset_search


app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the dataset explorer API.",
        "version": __version__,
        "links": [
            {"rel": "self", "href": "/"},
            {"rel": "datasets", "href": "/datasets"},
            {"rel": "dataset", "href": "/datasets/{builder_name}"},
        ]
    }


@app.get("/datasets")
async def list_datasets():
    return dataset_infos_by_name


@app.get("/dataset/{builder_name}")
async def get_dataset(builder_name: str):
    if builder_name not in dataset_infos_by_name:
        raise HTTPException(status_code=404, detail=f'Dataset "{builder_name}" not found.')
    return dataset_infos_by_name[builder_name]


@app.get("/search/{builder_name}")
async def search(builder_name: str, q: str=None, top: int=10):
    if builder_name not in dataset_infos_by_name:
        raise HTTPException(status_code=404, detail=f'Dataset "{builder_name}" not found.')

    return {
        "query": q,
        "results": dataset_search(builder_name, q, top=top) if q else [],
    }
