from __future__ import unicode_literals


class Parse(object):
    def __init__(self, nlp, text, collapse_punctuation, collapse_phrases):
        self.doc = nlp(text)
        if collapse_punctuation:
            spans = []
            for word in self.doc[:-1]:
                if word.is_punct:
                    continue
                if not word.nbor(1).is_punct:
                    continue
                start = word.i
                end = word.i + 1
                while end < len(self.doc) and self.doc[end].is_punct:
                    end += 1
                span = self.doc[start : end]
                spans.append(
                    (span.start_char, span.end_char,
                     {'tag': word.tag_, 'lemma': word.lemma_, 'ent_type': word.ent_type_})
                )
            for start, end, attrs in spans:
                self.doc.merge(start, end, **attrs)

        if collapse_phrases:
            for np in list(self.doc.noun_chunks):
                np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)

    def to_json(self):
        words = [{'text': w.text, 'tag': w.tag_} for w in self.doc]
        arcs = []
        for word in self.doc:
            if word.i < word.head.i:
                arcs.append(
                    {
                        'start': word.i,
                        'end': word.head.i,
                        'label': word.dep_,
                        'dir': 'left'
                    })
            elif word.i > word.head.i:
                arcs.append(
                    {
                        'start': word.head.i,
                        'end': word.i,
                        'label': word.dep_,
                        'dir': 'right'
                    })
        return {'words': words, 'arcs': arcs}


class Entities(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)
        print(self.doc)

    def to_json(self):
        return [{ 'word': str(ent), 'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
                for ent in self.doc.ents]
