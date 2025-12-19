# AMFinal
GitHub repo link: https://github.com/amonaghan715/AMFinal.git

**The Shakespeare Searcher**: Welcome to the Shakespeare Searcher! The Shakespeare Searcher is a tool that uses Word2Vec and FastText word embedding models to search through and generate text from a corpus of William Shakespeare's plays. Shakespeare's works have an unusually high density of poetic language and metaphor compared to modern texts, and the language used is also comparatively archaic. For these reasons, word embedding models trained on modern texts and larger corpuses offer lower quality results when used on Shakespearean text. The goal of this project was to change that by training word embedding models on a corpus that only contains Shakespearean language, and in doing so, hopefully provide a higher quality tool for searching and generating this specific style of text.

Author: Anna Monaghan

Course: Artificial Intelligence CSCI 2400

Date: 12/19/25

- why skipgram vs. cbow (the skip gram model predicts surroundings from words, ratehr than words from surroundings.
this is better when working with "rare" words or more uncommon language, which is important for Shakespeare).

# Table of Contents

**shakespeare_works**: A folder of text files containing all of William Shakespeare's plays.

**data.jsonl**: A json library file containing a json object for every line spoken in a Shakespeare play. This data is parsed from the text files in shakespeare_works, and is used both as the training corpus for the word embedding models, and to draw n-grams from for text generation.

**folder_loader.py**: A class that loads play text data from the text files provided, tokenizes said text data, and trains two models on it: a Word2Vec skip-gram model, and a FastText model.

**generator.py**: 

**main.py**: Contains the main function that runs the system.

**play_parser.py**: A Parser class, representing a single Parser object. Attributes include play_id, act, scene, speaker, text, lines, and object.

**searcher.py**: 

# Usage


# Installation Instructions and Requirements
- gensim (need to be in an environment that has gensim installed)

When you first run the system, you will be asked if you have ever used the tool before. If it is your first time running the program on your machine, or if you have deleted the data or model files, enter 'yes' or the 'y' character. The system will then take a moment to parse the text data from the shakespeare_works folder to the data file, and train the embeddings models on the data. From then on, anytime you rerun the system you can simply answer 'no or 'n' to that initial query, and the program will use the data and models that it has already stored and trained.

# Limitations and Biases
- This model has been trained and is constructed to function only on Shakespeare's plays, and not on his sonnets or other works.
- The model is trained on the plays as a whole and not inidividually on acts, so all meanings/neighbors of a word are clumped together. Thus, it does not account for shifts in meanings/symbolisms of words as a play progresses, nor does it have an understanding of the difference of words in different plays. For example, "blood" in a comedy might mean something very different from "blood" in a tragedy or a history, but all meanings and neighbors are treated equally in this model.
- The simlarity scores from the word2vec model are scored slgihtly higher. This is because fasttext model bases similarity score purely on word structure (which often pertains to semantics, but not always), and i wanted to account for the cases where spelling similarity does not mean semantic similarity.
- Trading some quality for the sake of domain specificity (comparitively small corpus)

# Acknowledgements
Gensim onine resource about FastText models: https://radimrehurek.com/gensim/auto_examples/tutorials/run_fasttext.html

A special thank you to Folger Digital Texts, the original source of the Shakespeare works used in this model. The only change made to these files was removing informational text from the beginning of each file pertaining to writing, editing, origin, file creation dates, and character information.
- Folger Creative Commons License: https://creativecommons.org/licenses/by-nc/3.0/
