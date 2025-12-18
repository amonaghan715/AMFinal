import json
import re
from pathlib import Path
from play_parser import Parser
from typing import Iterator, List
from gensim.models import Word2Vec
from gensim.models.fasttext import FastText

class Loader:
    """
    A class that loads play text data from the text files provided, tokenizes
    said text data, and trains two models on it: a Word2Vec skip-gram model,
    and a FastText model.
    
    Attributes: directory - the directory that holds the play files.
                data_file - the file to dump play text data to.
                plays - the list of play files in the directory.
                wv_model - the trained Word2Vec model.
                ft_model - the trained FastText model.
    """
    WORD_RE = re.compile(r"[a-z']+")
    SENTENCE_RE = re.compile(r"(?<=[.!?;:])\s+|\n+")

    def __init__(self, in_dir="shakespeare_works", out_json="data.jsonl"):
        """Initialize a Loader object."""
        self.directory = Path(in_dir)
        self.data_file = Path(out_json)
        self.plays = sorted(self.directory.glob("*.txt"))

        self.wv_model_path = "shakespeare_word2vec.model"
        self.wv_model = None
        self.ft_model_path = "shakespeare_fasttext.model"
        self.ft_model = None


    def get_plays(self):
        """Return the list of plays in the directory."""
        return self.plays
    

    def get_models(self):
        """Return the Word2Vec and FastText models."""
        self._train_models()
        return self.wv_model, self.ft_model


    def parse_folder(self):
        """
        Load the data from each play file in the folder to the data file.

        Args: None
        Returns: None
        """
        with self.data_file.open('w', encoding="utf-8") as file:
            for play in self.plays:
                parser = Parser(play.stem)
                for row in parser.parse_file(play):
                    file.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    
    def _train_models(self, train=False):
        """Train the Word2Vec model on the text from the data file."""
        # Load existing embedding models if not training.
        if not train:
            if self.wv_model_path.exists():
                self.wv_model = Word2Vec.load(self.wv_model_path)
        
            if self.ft_model_path.exists():
                self.ft_model = FastText.load(self.ft_model_path)
            return
        
        # Train the Word2Vec and FastText models on the text corpus.
        sentences = self._SentenceCorpus(self.data_file, Loader.SENTENCE_RE, Loader.WORD_RE)

        self.wv_model = Word2Vec(
            sentences=sentences,
            vector_size=200,
            window=8,
            min_count=3,
            workers=4,
            sg=1,
            negative=10)  
        self.wv_model.save(self.wv_model_path)

        self.ft_model = FastText(
            sentences=sentences,
            vector_size=200,
            window=8,
            min_count=3,
            workers=4,
            sg=1,
            negative=10,
            sample=1e-4,
            epochs=20)  
        self.ft_model.save(self.ft_model_path)


    class _SentenceCorpus:
        """DOCSTRING"""
        def __init__(self, data_file, sentence_re, word_re):
            self.data_file = data_file
            self.sentence_re = sentence_re
            self.word_re = word_re

        
        def __iter__(self):
            """DOCSTRING"""
            with self.data_file.open('r', encoding="utf-8") as file:
                for line in file:
                    row = json.loads(line)
                    for chunk in self.sentence_re.split(row["text"].strip()):
                        toks = self.word_re.findall(chunk.lower())
                        if toks:
                            yield toks
