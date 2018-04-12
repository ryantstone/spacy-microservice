# spacy-microservice

Spacy microservice is a barebones microservice specifically for receiving strings and returning results from Spacy's NER system.

## Setup
Add a .env file and a single attribute of `MODEL_NAME` with the path to the model if it's a directory or the name if it's been packaged and linked to Spacy. (I have not tested the latter)

## Run
`python app.py`

## Expectations
Post requests to the `/ent` route expects a json object with 1 attribute `text` with an array of strings. This will be processed and returned.
