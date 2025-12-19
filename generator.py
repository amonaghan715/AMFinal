"""
Author: Anna Monaghan
Course: Artificial Intelligence CSCI 2400
Assignment: Final Project
Date: 12/19/2025

Description: A text generator that uses tri-grams to make next word predictions
with Markov chains and leverages the word embedding models to bias towards words
that are "on-theme."
Known Bugs: None
"""
import json
import re
import random
from pathlib import Path
from collections import defaultDict, Counter

class Generator:
    """
    Represents a Generator object.
    
    Attributes: word_search - a word searcher object for finding word similarities.
                data_path - the path to the data file.
                order - 
                model - 
                starts - 
    """
    WORD_RE = re.compile(r"[a-z']+|[.,;:!?]")

    def __init__(self, word_search=None, data_path="data.jsonl"):
        """
        Initialize a Generator object.

        Args: data_path - the path to the data file.
        Returns: None
        """
        self.word_search = word_search
        self.data_path = Path(data_path)
        self.order = 3
        self.model = defaultDict(Counter)
        self.starts = []

        self._train


    def _tokenize(self, text):
        """Turn all of the words in the given text into individual tokens."""
        return Generator.WORD_RE.findall(text)
    

    def _train(self):
        """Build a Markov transition model based on words and context from the
        data file."""
        with self.data_path.open('r', encoding="utf-8") as file:
            for chunk in file:
                line = json.loads(chunk)
                text = line.get("text", "").strip()
                if not text:
                    continue
                    
                tokens = self._tokenize(text)
                if len(tokens) <= self.order:
                    continue

                # Record a plausible start for the line.
                self.starts.append(tuple(tokens[:self.order]))

                # Build transition model.
                for i in range(len(tokens) - self.order):
                    context = tuple(tokens[i:i + self.order])
                    next = tokens[i + self.order]
                    self.model[context][next] += 1

    
    def _sample_next(self, context):
        """Choose the next word in the line based on context words and the
        transition model."""
        choices = self.model.get(context)
        if not choices:
            return None
        
        # Make a weighted, random choice among the word options.
        total = sum(choices.values())
        r = random.randint(1, total)
        score = 0
        for word, count in choices.items():
            score += count
            if score >= r:
                return word
        return None
    

    def generate(self, max_tokens=30, theme=None, seed=None, alpha=1.5):
        """
        Generate a line of text based on the provided seed and the transition
        model.

        Args: max_tokens - the maximum number of tokens to generate to create
              a line with.
              seed - the seed word or words for the line to be generated from.
        Returns: A line of Shakespearean-esc text.
        """
        if seed:
            seed_tokens = self._tokenize(seed)
            if len(seed_tokens) >= self.order:
                context = tuple(seed_tokens[-self.order:])
            else:
                context = random.choice(self.starts)
        else:
            context = random.choice(self.starts)

        out = list(context)

        for _ in range(max_tokens - self.order):
            context = tuple(out[-self.order:])
            if theme:
                next = self._sample_next_themed(context, theme)
            else:
                next = self._sample_next(context)

            # Restart if a "dead end" is encountered.
            if next is None:
                out.extend(list(random.choice(self.starts)))
                continue
            out.append(next)

            if next in {".", "!", "?"} and len(out) > 9:
                break

        return self._detokenize(out)
    

    def _theme_similarity(self, theme, word):
        """Return similarity value between the given word and the theme (value
        between 0 and 1). Return 0 if not possible."""
        if not self.word_search or not theme:
            return 0
        
        similarity = float(self.word_search.similarity(word, theme))
        if similarity == 0:
            return 0
        
        # Return similarity score to 0,1 range.
        similarity = max(-1.0, min(1.0, similarity))
        return (similarity + 1) / 2.0
    

    def _sample_next_themed(self, context, theme, alpha=1.5):
        """Perform a weighted, random sample for the next word. Markov
        counts are boosted based on theme similarity. A higher alpha value
        puts more weight on theme similarity."""
        choices = self.model.get(context)
        if not choices:
            return None
        
        words = []
        weights = []

        for word, count in choices.items():
            similarity = self._theme_similarity(theme, word)
            weight = count * (1 + alpha + similarity)
            words.append(word)
            weights.append(weight)

        total = sum(weights)
        r = random.random() * total
        running_tot = 0.0
        for word, weight in zip(words, weights):
            running_tot += weight
            if running_tot >= r:
                return word
        return words[-1]
    

    def _detokenize(self, tokens):
        """Turn token list into a single sentence/line."""
        words = []

        for token in tokens:
            if token in {".", ",", ";", ":", "!", "?"}:
                if words:
                    words[-1] = words[-1] + token
                else:
                    words.append(token)
            else:
                words.append(token)
        
        text = " ".join(words)
        if text:
            return text.capitalize()
        return text
