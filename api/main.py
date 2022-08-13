"""
Entry point for the API.
"""
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from api.__version__ import __version__
from api.datasets import datasets_by_name


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
    return datasets_by_name


@app.get("/dataset/{builder_name}")
async def get_dataset(builder_name):
    if builder_name not in datasets_by_name:
        raise HTTPException(status_code=404, detail=f'Dataset "{builder_name}" not found.')
    return datasets_by_name[builder_name]
