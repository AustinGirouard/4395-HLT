import sys
import os

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint


'''
# Reads file from filepath
# Input: filepath
# Return: file data as text
'''
def read_file(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in


'''
# Processes tokenized text data by removing stopwords and non-alpha words, and removing words of length < 5
# Input: Raw data text
# Return: Tuple containing 
                1. Tokenized and processed set of words from text
                2. List of noun lemmas
'''
def processing(text):
    # Tokenize text with nltk library
    tokens = nltk.word_tokenize(text)
    # Lowercase all text
    tokens = [c.lower() for c in tokens]
    # Process out non-alpha words, stopwords, and short words
    tokens = [t for t in tokens if t.isalpha() and
              t not in stopwords.words('english') and
              len(t) > 5]

    # Lemmatize words
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    # Get list of unique lemmas
    unique_lemmas = list(set(lemmas))
    # Get POS tags of each unique lemma
    tags = nltk.pos_tag(unique_lemmas)
    # Display first 20 tagged lemmas
    print('The first 20 tagged lemmas:', tags[:20])

    # Create a list of lemmas which are nouns
    nouns = [k for k, v in tags if v == 'NN' or v == 'NNS' or v == 'NNP' or v == 'NNPS']

    # Print the number of tokens and the number of nouns
    print('Number of total tokens =', len(tokens))
    print('Number of nouns =', len(nouns))
    return tokens, nouns


'''
# Calculates the lexical diversity of a block of text
# Input: file data
# Return: lexical diversity as float (between 0 and 1)
'''
def lexical_diversity(text):
    # Make list of unique items from text list
    text_set = set(text)
    print('Unique:', len(text_set), 'Total:', len(text))
    return len(text_set)/len(text)


'''
# Executes an instance of the guessing game
# Input: List containing word bank
# Output: None
'''
def guessing_game(word_list):
    print('Welcome to the Word Guessing Game! Here are the rules: ')
    print('1) For every letter you guess correctly, 1 point is added to your score')
    print('2) For every letter you guess incorrectly, 1 point is deducted from your score')
    print('3) You start with 5 points. The game ends when:')
    print('\ta) You correctly guess the word\n\tb) Your score falls below 0\n\tc) You enter the ! character')
    print('\nGood luck!\n\n')

    # Initialize starting score 5
    score = 5
    # Initialize user_guess outside of scope
    user_guess = ''

    while user_guess != '!':
        # Select a random word from word list
        randWord = word_list[randint(0, 49)]

        # List to hold all letters guessed
        letters_guessed = []

        # Initialize current guessed letters as list, fill with underscores to start
        correct_guesses = []
        for i in range(len(randWord)):
            correct_guesses.append('_')

        # Start game
        while score >= 0 and user_guess != '!' and '_' in correct_guesses:
            # Display current correct guesses and all letters guessed
            print(*correct_guesses)
            print('Letter Guessed:', *letters_guessed)

            # Read letter guess input from user
            user_guess = input('\nGuess a letter:')

            # If user types nothing or types multiple letters, error and try again
            if len(user_guess) != 1 or not user_guess.isalpha():
                print('Invalid input. Try again. Score is', score)

            # if user types in a letter that has already been guessed, error and try again
            elif user_guess in letters_guessed:
                print('You already guessed that letter! Try again. Score is', score)

            # User guesses correct letter
            elif user_guess in randWord:
                # Add letter to list of guessed letters and increment score
                letters_guessed.append(user_guess)
                score += 1
                print('Right! Score is', score)
                # For loop to update list of correct guesses with current guess
                for i in range(len(randWord)):
                    if randWord[i] == user_guess:
                        correct_guesses[i] = user_guess

            # User guesses incorrect letter
            else:
                # Add letter to list of guessed letters and decrement score
                letters_guessed.append(user_guess)
                score -= 1
                print("Sorry, guess again. Score is", score)

        print('\n')
        print(*correct_guesses)

        # If score is > 0, user must have solved it
        if score > 0:
            print('You solved it!')

        # If input is !, user terminated program
        if user_guess == '!':
            print('Game terminated.')
            break

        if score < 0:
            print('You failed.')
            print('The word was', randWord.upper())
            break

        print('\nCurrent score =', score)
        print('#############################################\n')

    print('\nFinal score = ', score)


def main():
    # If no filepath is entered, print error and quit
    if len(sys.argv) < 2:
        print('Error. Please enter a filename as a system arg.')
        quit()

    fp = sys.argv[1]
    data = read_file(fp)

    # Tokenize data with no processing
    unclean_tokens = nltk.word_tokenize(data)
    # Calculate lexical diversity of tokenized data
    unclean_lex_div = lexical_diversity(unclean_tokens)
    print('Unprocessed tokenized lexical diversity = {:.2f}'.format(unclean_lex_div))

    # Process text data
    # Result holds a tuple containing the processed data and a list of noun lemmas
    result = processing(data)

    # Unpack tuple
    (tokens, nouns) = result

    # Create a dictionary from nouns and tokens which has
    # noun:noun of nouns in tokens list
    nouns_dict = {}
    for t in tokens:                        # Loop through tokens
        if t in nouns:                      # Check if token is a noun
            if t not in nouns_dict:         # Count noun in dictionary
                nouns_dict[t] = 1
            else:
                nouns_dict[t] += 1

    # Sort and store the top 50 most common nouns into most_common_nouns
    most_common_nouns = sorted(nouns_dict, key=nouns_dict.get, reverse=True)[:50]

    # Print top 50 most common nouns and their counts
    for k in most_common_nouns:
        print(k, ':', nouns_dict[k])

    # Start Guessing Game
    while True:
        user_response = input('Want to play the Guessing Game? (Enter to continue; n to quit): ')
        if user_response.lower() == 'n':
            break
        else:
            guessing_game(most_common_nouns)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
