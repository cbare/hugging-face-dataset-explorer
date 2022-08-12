# Medical question pairs

Demo using the dataset [medical_questions_pairs][1], a semantic similarity dataset consisting of 3048 similar and dissimilar medical question pairs hand-generated and labeled by Curai's doctors.


## Development

To run the api:

>> uvicorn api.main:app --reload

>> http http://127.0.0.1:8000


[1]: https://huggingface.co/datasets/medical_questions_pairs
