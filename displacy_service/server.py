#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

from pathlib import Path
import falcon
import spacy
import json
from dotenv import load_dotenv, find_dotenv
import os

from spacy.symbols import ENT_TYPE, TAG, DEP

import spacy.util

from .parse import Parse, Entities

load_dotenv(find_dotenv())
MODELS = spacy.util.LANGUAGES.keys()
MODEL = os.environ.get('MODEL_NAME')

try:
    unicode
except NameError:
    unicode = str


_models = {}


def get_model(model_name):
    if model_name not in _models:
        _models[model_name] = spacy.load(model_name)
    return _models[model_name]


def get_ent_types(model):
    '''List the available entity types in the model.'''
    labels = set()
    for move_name in model.parser.moves.move_names:
        labels.add(move_name.split('-')[-1])
        print(labels)
    return sorted(list(labels))


class EntResource(object):
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        texts = json_data.get('text')
        entities = []
        for text in texts:
            entities.append(EntResource.detect_entities(self, text))
        print(entities)

    def detect_entities(self, text):
        try:
            model = get_model(MODEL)
            entities = Entities(model, text)
            return entities.to_json
        except Exception:
            raise Exception


APP = falcon.API()
APP.add_route('/ent', EntResource())
