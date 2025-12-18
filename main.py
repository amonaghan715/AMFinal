from folder_loader import Loader
from search import Searcher

def main():
    """The main function to run the system."""
    loader = Loader()
    loader.parse_folder()
    wv_model, ft_model = loader.get_models()
    searcher = Searcher(wv_model, ft_model)

    while(True):
        input_word = input("Please enter a word to search for: ")
        words = searcher.n_similar_words(input_word, 5)

        if words:
            print(words)
        else:
            print("Unknown word. Please try a different one.\n")


if __name__ == "__main__":
    main()
    