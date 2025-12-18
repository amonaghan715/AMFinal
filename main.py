from folder_loader import Loader
from searcher import WordSearcher, LineSearcher

def main():
    """The main function to run the system."""
    print("Welcome to the Shakespeare Searcher!")
    answer = input("Hast thou used this fine tool before? (y/n): ")

    load_and_train = True
    if "y" in answer.lower():
        load_and_train = False

    keepGoing = True
    data_file = "data.jsonl"
    loader = Loader(load_and_train)
    loader.parse_folder()
    wv_model, ft_model = loader.get_models()

    word_search = WordSearcher(wv_model, ft_model)
    line_search = LineSearcher(data_file, word_search)

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

                words = word_search.n_similar_words(input_word, 7)
                if words:
                    for word, score in words:
                        print(f"{word} (Similarity score: {round(score, 3)})")
                else:
                    print("Unknown word.\nWouldst thou provide a synonym?\n")
                    repeat = True
            print("\n")
        elif "2" in action:
            repeat = True
            while(repeat):
                repeat = False
                search_word = input("Please enter a theme to search for: ")

                filters = {}
                query = input("Would you like to add a search filter? (y/n): ").strip()
                if "y" in query.lower():
                    tag = input("Enter the filter tag (options: play_id, speaker, act, scene): ").strip()
                    spec = input("Enter your specification (romeo-and-juliet, JULIET, 3, etc.): ").strip()

                    # Clean tag and spec entries to match expected forms.
                    if tag == 'play_id':
                        spec = spec.lower()
                    elif tag == 'speaker':
                        spec = spec.upper()
                    elif tag == 'act' or tag == 'scene':
                        spec = int(spec)

                    filters[tag] = spec
                
                print("\n")
                hits = line_search.search(query=search_word, expand=True, filters=filters)
                if hits:
                    for hit in hits:
                        print(hit)
                        print("\n")
                else:
                    print("Unknown word or no lines that match that theme.")
                    print("Wouldst thou provide a synonym?\n")
                    repeat = True
        #elif "3" in action:
            
        else:
            print("Unknown action. Please enter the action you would like to take.\n")


if __name__ == "__main__":
    main()
