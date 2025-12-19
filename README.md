# Anna Monaghan Final Project
GitHub repo link: https://github.com/amonaghan715/AMFinal.git

**The Shakespeare Searcher**: Welcome to the Shakespeare Searcher! The Shakespeare Searcher is a tool that uses Word2Vec and FastText word embedding models to search through and generate text from a corpus of William Shakespeare's plays. Shakespeare's works have an unusually high density of poetic language and metaphor compared to modern texts, and the language used is also comparatively archaic. For these reasons, word embedding models trained on modern texts and larger corpuses offer lower quality results when used on Shakespearean text. The goal of this project was to change that by training word embedding models on a corpus that only contains Shakespearean language, and in doing so, hopefully provide a higher quality tool for searching and generating this specific style of text.

Author: Anna Monaghan

Course: Artificial Intelligence CSCI 2400

Date: 12/19/25

# Table of Contents

**shakespeare_works**: A folder of text files containing all of William Shakespeare's plays.

**data.jsonl**: A json library file containing a json object for every line spoken in a Shakespeare play. This data is parsed from the text files in shakespeare_works, and is used both as the training corpus for the word embedding models, and to draw n-grams from for text generation.

**folder_loader.py**: A class that loads play text data from the text files provided, tokenizes said text data, and trains two models on it: a Word2Vec skip-gram model, and a FastText model.

**generator.py**: A Generator class, representing a Generator object. Attributes include word_search, data_path, order, model, and starts.

**main.py**: Contains the main function that runs the system.

**play_parser.py**: A Parser class, representing a single Parser object. Attributes include play_id, act, scene, speaker, text, lines, and object.

**searcher.py**: Contains the WordSearcher, LineSearcher, and SearchHit classes, representing their respective objects. WordSearcher is used for individual word semantics, and LineSearcher for semantics over a whole passage/line. SearchHit is used for representing and displaying lines from the data file in the main loop.

# Installation Instructions and Requirements
This system must be run in an environment that has gensim installed in order for the word embedding models to work.

If gensim is not installed in your environment, run the command: python3 -m pip install gensim

When you first run the system, you will be asked if you have ever used the tool before. If it is your first time running the program on your machine, or if you have deleted the data or model files, enter 'yes' or the 'y' character. The system will then take a moment to parse the text data from the shakespeare_works folder to the data file, and train the embeddings models on the data. From then on, anytime you rerun the system you can simply answer 'no or 'n' to that initial query, and the program will use the data and models that it has already stored and trained.

# Limitations and Biases
This model is, of course, not perfect, and has a few limitations and biases.
- The model is trained on the Shakespeare's plays as a whole, and not individually on each genre (tragedy, comedy, history). Thus, it does not account for shifts in meanings of words in different plays. For example, "blood" in a comedy might mean something very different from "blood" in a tragedy or in a history, but all meanings and neighbors are treated equally by the model.
- In seeking to achieve a high degree of domain specificity with this model, I have traded breadth of vocabulary. Many words that one might want to search for that are common in our modern language (such as "hello") are not present in the training corpus, and therefore are missing from the model.

# Acknowledgements
Gensim onine resource about FastText models: https://radimrehurek.com/gensim/auto_examples/tutorials/run_fasttext.html

A special thank you to Folger Digital Texts, the original source of the Shakespeare works used in this model. The only change made to these files was removing informational text from the beginning of each file pertaining to writing, editing, origin, file creation dates, and character information.
- Folger Creative Commons License: https://creativecommons.org/licenses/by-nc/3.0/
