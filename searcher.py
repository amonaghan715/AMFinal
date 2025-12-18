import json
import math
import re
import numpy as np
from pathlib import Path

class WordSearcher:
    """DOCSTRING"""

    def __init__(self, wv_model, ft_model):
        self.wv_model = wv_model
        self.ft_model = ft_model
    

    def n_similar_words(self, in_word: str, n: int):
        """
        Find the n most similar words to the input word based on combined
        scores from the two trained models, with the score from the Word2Vec
        model weighted slightly higher.
        
        Args: in_word - the input word to find similarities for.
              n - the number of most similar words to return.
        Returns: a list of the n most similar words to in_word.
        """
        in_word = in_word.lower()
        similar_words = {}

        if in_word in self.wv_model.wv:
            similar_words = {word : score * 0.7 for word, score in
                             self.wv_model.wv.most_similar(in_word, topn=50)}
        
        if in_word in self.ft_model.wv:
            for word, score in self.ft_model.wv.most_similar(in_word, topn=50):
                if word in similar_words:
                    similar_words[word] += score * 0.3
                else:
                    similar_words[word] = score * 0.3

        sorted_similars = sorted(similar_words.items(), key=lambda x: x[1], reverse=True)
        return sorted_similars[:n]


class LineSearcher:
    """DOCSTRING"""

    WORD_RE = re.compile(r"[a-z']+")
    
    def __init__(self, data_path: str, word_search=None):
        """DOCSTRING"""
        self.data_path = Path(data_path)
        self.word_search = word_search
    
        self.lines = []
        self.tf_per_line = []
        self.doc_freq = {}
        self.num_lines = 0

        self._load()
        self._compute_doc_freq()

    
    def _tokenize(self, text: str):
        """DOCSTRING"""
        return LineSearcher.WORD_RE.findall(text.lower())
    

    def _load(self):
        """DOCSTRING"""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Could not find data file: {self.data_path}")
        
        with self.data_path.open('r', encoding="utf-8") as file:
            for chunk in file:
                chunk = chunk.strip()
                if not chunk:
                    continue
                line = json.loads(chunk)
                
                text = line.get("text", "")
                token_freq = {}
                for token in self._tokenize(text):
                    token_freq[token] = token_freq.get(token, 0) + 1

                self.lines.append(line)
                self.tf_per_line.append(token_freq)
        
        self.num_lines = len(self.lines)

    
    def _compute_doc_freq(self):
        """DOCSTRING"""
        for tokens in self.tf_per_line:
            for token in tokens.keys():
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1


    def _idf(self, token: str):
        """DOCSTRING"""
        return math.log((self.num_lines + 1) / (self.doc_freq.get(token, 0) + 1))
    

    def _expand_query_tokens(self, query: str, n=6):
        """DOCSTRING"""
        tokens = self._tokenize(query)
        if not self.word_search or not tokens:
            return tokens
        
        base = tokens[0]
        expanded = list(tokens)

        try:
            for w, _score in self.word_search.n_similar_words(base, n):
                expanded.append(w)
        except Exception:
            pass

        return expanded


    def search(self, query: str, top_k=5, expand=True, expand_n=6, filters=None):
        """DOCSTRING"""
        if not query or not query.strip():
            return []
        
        query_tokens = []
        if expand:
            query_tokens = self._expand_query_tokens(query, expand_n)
        else:
            query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        scores = []
        for i, (line, tf) in enumerate(zip(self.lines, self.tf_per_line)):
            if filters:
                ok = True
                for key, val, in filters.items():
                    if line.get(key) != val:
                        ok = False
                        break
                if not ok:
                    continue

            score = 0.0
            for qt in query_tokens:
                c = tf.get(qt, 0)
                if c:
                    score += c * self._idf(qt)
            if score > 0:
                scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [SearchHit(score, self.lines[i]) for i, score in scores[:top_k]]
    

class SearchHit:
    """DOCSTRING"""
    def __init__(self, score, line):
        """DOCSTRING"""
        self.score = score
        self.line = line

    
    def __str__(self):
        """Return a printable representaion of a SearchHit object."""
        play_id = self.line.get('play_id')
        act = self.line.get('act')
        scene = self.line.get('scene')
        speaker = self.line.get('speaker')
        text = self.line.get('text')

        new_play_id = play_id.replace("-", " ")
        new_play_id = new_play_id.title()

        printable = f"{new_play_id}, Act {act}, Scene {scene}\n{speaker}: {text}"
        return printable

