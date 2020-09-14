from pathlib import Path
import csv
import random

from .util import get_file
from ._registry import register_loader


# DBPedia Ontology from https://course.fast.ai/datasets
DBPEDIA_ONTOLOGY_URL = "https://s3.amazonaws.com/fast-ai-nlp/dbpedia_csv.tgz"


@register_loader("dbpedia")
def dbpedia(train=True, loc=None, *, limit=0, shuffle=True):
    if loc is None:
        loc = get_file("dbpedia_csv", DBPEDIA_ONTOLOGY_URL, untar=True, unzip=True)
    data_loc = Path(loc) / "test.csv"
    if train:
        data_loc = Path(loc) / "train.csv"
    return read_dbpedia_ontology(data_loc, limit=limit, shuffle=shuffle)


def read_dbpedia_ontology(data_file, *, limit=0, shuffle=True):
    examples = []
    with open(data_file, newline="", encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            label = row[0]
            title = row[1]
            text = row[2]
            examples.append((title + "\n" + text, label))
    if shuffle:
        random.shuffle(examples)
    if limit >= 1:
        examples = examples[:limit]
    return examples
