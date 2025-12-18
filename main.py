from folder_loader import Loader
from searcher import Searcher

def main():
    """The main function to run the system."""
    print("Welcome to the Shakespeare Searcher!")
    answer = input("Hast thou used this fine tool before? (y/n): ")

    load_and_train = True
    if "y" in answer.lower():
        load_and_train = False

    keepGoing = True
    loader = Loader(load_and_train)
    loader.parse_folder()
    wv_model, ft_model = loader.get_models()
    searcher = Searcher(wv_model, ft_model)

    while(keepGoing):
        print("1. Run the Shakespearean thesaurus")
        print("2. Find lines related to a theme")
        print("3. Generate a line of Shakespeare-inspired text")
        action = input("What wouldst thou like to do? ")

        if "1" in action:
            repeat = True
            while(repeat):
                repeat = False
                input_word = input("Please enter a word to search for: ")

                words = searcher.n_similar_words(input_word, 7)
                if words:
                    for word, score in words:
                        print(f"{word} (Similarity score: {round(score, 3)})")
                else:
                    print("Unknown word. Wouldst thou provide a synonym?\n")
                    repeat = True
                print("\n")
        #elif "2" in action:



if __name__ == "__main__":
    main()
