import re
import nltk
from nltk.corpus import words
import random


nltk.download('words')

# Get the list of words
word_list = words.words()

# Define a regex pattern
pattern = re.compile(r'^[a-z]{5}$')  # Example: words with exactly 5 lowercase letters

# Search for words matching the pattern
matching_words = [word for word in word_list if pattern.match(word)]

# Print the matching words
print(len(matching_words))

dictionary_size = len(matching_words)
random_index = random.randint(0, dictionary_size - 1)
guess = matching_words[random_index]

print(guess)

guess_param = {
    "guess": guess,
    "excluded_letters": "",
    "correct_letters": "",
    "correct_positions": [0,0,0,0,0]
}


def generate_list(guess_param, word_list):
    search_expression = f"^[^{guess_param['excluded_letters']}]{{5}}$"
    pattern = re.compile(search_expression)
    matching_words = [word for word in word_list if pattern.match(word)]
    print(len(matching_words))
    return matching_words


def update_parameters(guess_param, feedback):
    for index, result in enumerate(feedback):
        letter = guess_param["guess"][index]
        if result == "2":
            print("Correct letter and position")
            guess_param["correct_positions"][index] = letter
        elif result == "1":
            print("Correct letter but wrong position")
            if letter not in guess_param["correct_letters"]:
                guess_param["correct_letters"] += letter
        else:
            print("Wrong letter")
            if letter not in guess_param["excluded_letters"]:
                guess_param["excluded_letters"] += letter
    print(guess_param)


feedback = 00000
while feedback != 22222:
    print("Input 2 for correct letter and position, 1 for correct letter and wrong position, 0 for wrong letter: ")
    feedback = input(": ")
    update_parameters(guess_param, feedback)
    matching_words = generate_list(guess_param, matching_words)
    random_index = random.randint(0, len(matching_words) - 1)
    guess = matching_words[random_index]
    guess_param["guess"] = guess
    print(guess)







