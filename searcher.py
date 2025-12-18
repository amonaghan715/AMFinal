class Searcher:
    """DOCSTRING"""

    def __init__(self, wv_model, ft_model):
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
    