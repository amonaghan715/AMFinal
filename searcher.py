"""
Author: Anna Monaghan
Course: Artificial Intelligence CSCI 2400
Assignment: Final Project
Date: 12/19/2025

Description: Contains the WordSearcher, LineSearcher, and SearchHit classes, representing
their respective objects. WordSearcher is used in searching for similarities between
individual words, and LineSearcher for theme-relatedness over a whole passage/line. SearchHit
is used for representing and displaying lines from the data file in the main loop.
Known Bugs: None
"""
import json
import math
import re
from pathlib import Path

class WordSearcher:
    """
    Represents a WordSearcher object, used for finding similar words among the
    training corpus and scoring word similarities.

    Attributes: wv_model - the trained Word2Vec model for assessing semantic
                similarity.
                ft_model - the trained FastText model for assessing semantic
                similarity.
    """

    def __init__(self, wv_model, ft_model):
        """
        Initialize a WordSearcher object.

        Args: wv_model - the trained Word2Vec model.
              ft_model - the trained FastText model.
        """
        self.wv_model = wv_model
        self.ft_model = ft_model
    

    def n_similar_words(self, in_word, n):
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

        # Find the most similar words based on the Word2Vec model
        if in_word in self.wv_model.wv:
            similar_words = {word : score * 0.7 for word, score in
                             self.wv_model.wv.most_similar(in_word, topn=50)}
        
        # Find the most similar words based on the FastText model.
        if in_word in self.ft_model.wv:
            for word, score in self.ft_model.wv.most_similar(in_word, topn=50):
                if word in similar_words:
                    similar_words[word] += score * 0.3
                else:
                    similar_words[word] = score * 0.3

        # Sort candidate words from highest to lowest by combined score.
        sorted_similars = sorted(similar_words.items(), key=lambda x: x[1], reverse=True)
        return sorted_similars[:n]
    

    def similarity(self, word1, word2):
        """
        Return the similarity score between the input words. This method
        weights the FastText model score slightly higher, as FastText is
        better at handling out-of-vocabulary words.
        
        Args: word1, word2 - the input words to be compared.
        Returns: The similarity score (between 0 and 1) of the input words.
        """
        score = 0
        word1 = word1.lower()
        word2 = word2.lower()

        score += self.ft_model.wv.similarity(word1, word2) * 0.6

        if word1 in self.wv_model.wv and word2 in self.wv_model.wv:
            score += self.wv_model.wv.similarity(word1, word2) * 0.4
        
        if score == 0:
            print("One or both of the given words was not known by the model.\n")
        return score


class LineSearcher:
    """
    Represents a LineSearcher object, used to search lines/passages related
    to a given theme.

    Attributes: data_path - the path to the data file.
                word_search - a WordSearcher object to use for searching related words.
                lines - a list of line dictionaries from the data file.
                tf_per_line - a list of term frequency dictionaries align with lines.
                doc_freq - a dictionary mapping tokens to the number of lines containing it.
                num_lines - the total number of lines in the corpus.
    """

    WORD_RE = re.compile(r"[a-z']+")
    
    def __init__(self, data_path, word_search=None):
        """
        Initialize a LinSearcher object.
        
        Args: data_path - the path to the data file.
              wrd_search - an optional WordSearcher object.
        """
        self.data_path = Path(data_path)
        self.word_search = word_search
    
        self.lines = []
        self.tf_per_line = []
        self.doc_freq = {}
        self.num_lines = 0

        self._load()
        self._compute_doc_freq()

    
    def _tokenize(self, text):
        """Turn all of the words in the given text into individual tokens."""
        return LineSearcher.WORD_RE.findall(text.lower())
    

    def _load(self):
        """Take each line from the data file and make a term frequency dictionary
        from its tokenized text. Add the line and dictionary to their appropriate
        list attributes."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Could not find data file: {self.data_path}")
        
        with self.data_path.open('r', encoding="utf-8") as file:
            for chunk in file:
                chunk = chunk.strip()
                if not chunk:
                    continue
                line = json.loads(chunk)
                
                text = line.get("text", "")
                term_freq = {}
                for token in self._tokenize(text):
                    term_freq[token] = term_freq.get(token, 0) + 1

                self.lines.append(line)
                self.tf_per_line.append(term_freq)
        
        self.num_lines = len(self.lines)

    
    def _compute_doc_freq(self):
        """Count the number of lines containing each token in the current
        line and add it to the document frequency dictionary."""
        for tokens in self.tf_per_line:
            for token in tokens.keys():
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1


    def _idf(self, token):
        """Find the inverse document frequency of the given token to assess
        the impact of a line (less common words have more impact)."""
        return math.log((self.num_lines + 1) / (self.doc_freq.get(token, 0) + 1))
    

    def _expand_query_tokens(self, query, n=6):
        """Expand the query token to n similar words to widen search."""
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


    def search(self, query, top_k=5, expand=True, expand_n=6, filters=None):
        """
        Search for the most similar/on-theme passages to the input word based
        on tf-idf and token similarity.

        Args: query - the word to relate passages to.
              top_k - the number of most on-theme passages to return
              expand - whether or not to expand the search using query-related words.
              expand_n - the number of related words to expand to.
              filters - optional search filters to be applied to candidate passages.
        Returns: A list of SearchHit objects for the top k most on-theme passages.
        """
        if not query or not query.strip():
            return []
        
        # Expand the search to other themed words.
        query_tokens = []
        if expand:
            query_tokens = self._expand_query_tokens(query, expand_n)
        else:
            query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        # Give each line a tf-idf score in order to return the most related passages.
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
    """
    A class representing a SearchHit object, used in the LineSearch class,
    and to display passages in the main loop.
    
    Attributes: score - The similarity score of the input line.
                line - The input line from the data file, including text and tags.
    """
    def __init__(self, score, line):
        """
        Initialize a SearchHit object.
        
        Args: score, line.
        """
        self.score = score
        self.line = line

    
    def __str__(self):
        """Return a printable representation of a SearchHit object."""
        play_id = self.line.get('play_id')
        act = self.line.get('act')
        scene = self.line.get('scene')
        speaker = self.line.get('speaker')
        text = self.line.get('text')

        new_play_id = play_id.replace("-", " ")
        new_play_id = new_play_id.title()

        printable = f"{new_play_id}, Act {act}, Scene {scene}\n{speaker}: {text}"
        return printable
