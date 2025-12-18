# AMFinal
- why skipgram vs. cbow (the skip gram model predicts surroundings from words, ratehr than words from surroundings.
this is better when working with "rare" words or more uncommon language, which is important for Shakespeare).

# Limitations and Biases
- This model has been trained and is constructed to function only on Shakespeare's plays, and not on his sonnets or other works.
- The model is trained on the plays as a whole and not inidividually on acts, so all meanings/neighbors of a word are clumped together. Thus, it does not account for shifts in meanings/symbolisms of words as a play progresses, nor does it have an understanding of the difference of words in different plays. For example, "blood" in a comedy might mean something very different from "blood" in a tragedy or a history, but all meanings and neighbors are treated equally in this model.
- The simlarity scores from the word2vec model are scored slgihtly higher. This is because fasttext model bases similarity score purely on word structure (which often pertains to semantics, but not always), and i wanted to account for the cases where spelling similarity does not mean semantic similarity.

# Installation Instructions and Requirements
- gensim (need to be in an environment that has gensim installed)

When you first run the system, you will be asked if you have ever used the tool before. If it is your first time running the program on your machine, or if you have deleted the data or model files, enter 'yes' or the 'y' character. The system will then take a moment to parse the text data from the shakespeare_works folder to the data file, and train the embeddings models on the data. From then on, anytime you rerun the system you can simply answer 'no or 'n' to that initial query, and the program will use the data and models that it has already stored and trained.

# TODOS
- Add genre tags
- user interaction
- create search mechanism
- use second model for modern langauge command processing?
- README
- docstrings and documentation

# Acknowledgements
Gensim onine resource about FastText models: https://radimrehurek.com/gensim/auto_examples/tutorials/run_fasttext.html

The original source of the Shakespeare works used in this model was Folger Digital Texts. The only change made to these files was removing informational text from the beginning of each file pertaining to writing, editing, origin, file creation dates, and character information.
- Folger Creative Commons Liscense: https://creativecommons.org/licenses/by-nc/3.0/

# To dos
- Search for related lines
- Generate text
