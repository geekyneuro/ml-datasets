import json
from pathlib import Path
import random
import csv

from .util import get_file
from ._registry import register_loader

CMU_URL = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"


@register_loader("cmu")
def cmu(loc=None, limit=0):
    if loc is None:
        loc = get_file("MovieSummaries", CMU_URL, untar=True, unzip=True)
    meta_loc = Path(loc) / "movie.metadata.tsv"
    text_loc = Path(loc) / "plot_summaries.txt"
    return read_cmu(meta_loc, text_loc, limit=limit), []


def read_cmu(meta_loc, text_loc, limit=0, shuffle=True):
    examples = []
    genre_by_id = {}
    title_by_id = {}
    with meta_loc.open("r", encoding="utf8") as file_:
        for row in csv.reader(file_, delimiter="\t"):
            movie_id = row[0]
            title = row[2]
            annot = row[8]
            d = json.loads(annot)
            genres = set(d.values())
            genre_by_id[movie_id] = genres
            title_by_id[movie_id] = title

    with text_loc.open("r", encoding="utf8") as file_:
        for row in csv.reader(file_, delimiter="\t"):
            movie_id = row[0]
            text = row[1]
            genres = genre_by_id.get(movie_id, None)
            title = title_by_id.get(movie_id, "")
            if genres:
                examples.append((title + "\n" + text, genres))

    if shuffle:
        random.shuffle(examples)
    if limit >= 1:
        examples = examples[:limit]

    return examples
