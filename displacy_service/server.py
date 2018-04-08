#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

from pathlib import Path
import falcon
import spacy
import json
import os

from spacy.symbols import ENT_TYPE, TAG, DEP

import spacy.util

from .parse import Parse, Entities


MODELS = spacy.util.LANGUAGES.keys()
MODEL = os.environ['MODEL_NAME']

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
    """Parse text and return displaCy ent's expected output."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        model_name = _model
        try:
            model = get_model(model_name)
            entities = Entities(model, text)
            print(text)
            print(model_name)
            print(entities.to_json())
            import code; code.interact(local=dict(globals(), **locals()))
            resp.body = json.dumps(entities.to_json(), sort_keys=True,
                                   indent=2)
            resp.content_type = 'text/string'
            resp.append_header('Access-Control-Allow-Origin', "*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500


APP = falcon.API()
APP.add_route('/ent', EntResource())
