"""
Author: Anna Monaghan
Course: Artificial Intelligence CSCI 2400
Assignment: Final Project
Date: 12/19/2025

Description: A class that loads play text data from the text files provided,
tokenizes said text data, and trains two models on it: a Word2Vec skip-gram
model, and a FastText model.
Known Bugs: None
"""
import json
import re
from pathlib import Path
from play_parser import Parser
from gensim.models import Word2Vec
from gensim.models.fasttext import FastText

class Loader:
    """
    Represents a Loader object, used for loading play data and training
    embedding models.
    
    Attributes: directory - the directory that holds the play files.
                data_file - the file to dump play text data to.
                plays - the list of play files in the directory.
                wv_model - the trained Word2Vec model.
                ft_model - the trained FastText model.
    """
    WORD_RE = re.compile(r"[a-z']+")
    SENTENCE_RE = re.compile(r"(?<=[.!?;:])\s+|\n+")

    def __init__(self, load_and_train, in_dir="shakespeare_works", out_json="data.jsonl"):
        """
        Initialize a Loader object.
        
        Args: load_and_train - whether to load the play data to the data file
              and train the word embedding models, or use stored data/models.
              in_dir - the path to the directory holding the plays.
              out_json - the path to the jsonl file that will hold the play data.
        """
        self.load_data = load_and_train
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
        # Only parse data from plays folder if the data file does not already exist.
        if self.data_file.exists() and not self.load_data:
            return
        
        with self.data_file.open('w', encoding="utf-8") as file:
            for play in self.plays:
                parser = Parser(play.stem)
                for row in parser.parse_file(play):
                    file.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    
    def _train_models(self):
        """Train the Word2Vec and FastText models on the text from the data file."""
        # Load embedding models if they exist already.
        if not self.load_data:
            if self.wv_model_path:
                self.wv_model = Word2Vec.load(self.wv_model_path)
        
            if self.ft_model_path:
                self.ft_model = FastText.load(self.ft_model_path)
            return
        
        # Train the Word2Vec and FastText models on the text corpus if they do not already exist.
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
        """
        An inner class for Loader objects, used to represent each line/sentence
        from the given play file as a list of tokens.
        
        Attributes: data_file - the file that stores the text of the.
                    sentence_re - the regex pattern used to identify lines/sentences.
                    word_rd - the regex pattern used to identify words.
        """
        def __init__(self, data_file, sentence_re, word_re):
            """
            Initialize a SentenceCorpus object.

            Args: data_file, sentence_re, word_re.
            """
            self.data_file = data_file
            self.sentence_re = sentence_re
            self.word_re = word_re

        
        def __iter__(self):
            """Take each line from the given play file and split it into
            a list of word tokens."""
            with self.data_file.open('r', encoding="utf-8") as file:
                for line in file:
                    row = json.loads(line)
                    for chunk in self.sentence_re.split(row["text"].strip()):
                        tokens = self.word_re.findall(chunk.lower())
                        if tokens:
                            yield tokens
