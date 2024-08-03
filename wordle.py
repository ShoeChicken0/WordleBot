import re
import nltk
from nltk.corpus import words
import random
import enchant

nltk.download('words')
dictionary = enchant.Dict("en_US")
# Get the list of words
word_list = words.words()
pattern = re.compile(r'^(?!.*(.).*\1)[a-z]{5}$')
five_letter_words = [word for word in word_list if pattern.match(word)]
print(f"nltk word list: {len(five_letter_words)}")
matching_words = [word for word in five_letter_words if dictionary.check(word)]
dictionary_size = len(matching_words)
print(f"valid word list: {dictionary_size}")
random_index = random.randint(0, dictionary_size - 1)
guess = matching_words[random_index]
print(guess)

guess_param = {
    "guess": guess,
    "excluded_letters": "",
    "correct_letters": [],
    "correct_positions": ["0","0","0","0","0"]
}

# regex for letters that must be included
def correct_expression(guess_param):
    correct_regex = ""
    for correct_letter in guess_param["correct_letters"]:
        correct_regex += f"(?=.*{correct_letter})"
    return correct_regex
        

# filter the list of words based on regex pattern from guess param
def generate_list(guess_param, word_list):
    include_letters = correct_expression(guess_param)
    exclude_letters = f"[^{guess_param["excluded_letters"]}]"
    correct_letters = ""
    search_expression = ""
    # counters for consecutive letter inclusion/exclusion (counter1) and correct position (counter2)
    counter1 = 0
    counter2 = 0
    position2 = 0

    for index, position in enumerate(guess_param["correct_positions"]):
        if position == "0":
            if index == 0:
                counter1 += 1

            else:
                counter1 += 1
                if counter2 > 0:
                    for i in range(counter2):
                        correct_letters += guess_param["correct_positions"][position2+i]
                    search_expression += f"{correct_letters}"
                    counter2 = 0
            if index == 4:
                search_expression += f"{include_letters}{exclude_letters}{{{counter1}}}$"
        else:
            if index == 0:
                counter2 += 1
                position2 = index
            else:
                if counter2 == 0:
                    position2 = index
                counter2 += 1
                if counter1 > 0:
                    search_expression += f"{include_letters}{exclude_letters}{{{counter1}}}"
                    counter1 = 0
            if index == 4:
                for i in range(counter2):
                    correct_letters += guess_param["correct_positions"][position2+i]
                    search_expression += f"{correct_letters}$"

    #search_expression = f"{include_letters}^[^{guess_param['excluded_letters']}]{{5}}$"
    print(search_expression)
    pattern = re.compile(search_expression)
    matching_words = [word for word in word_list if pattern.match(word)]

    print(len(matching_words))
    return matching_words

# update the guess parameters based on feedback
def update_parameters(guess_param, feedback):
    for index, result in enumerate(feedback):
        letter = guess_param["guess"][index]

        if result == "2":
            print("Correct letter and position")
            guess_param["correct_positions"][index] = letter
            # if the letter is both correct and position remove from correct letter and move to position
            if letter in guess_param["correct_letters"]:
                guess_param["correct_letters"].remove(letter)

        elif result == "1":
            print("Correct letter but wrong position")
            if letter not in guess_param["correct_letters"] and letter not in guess_param["correct_positions"]:
                guess_param["correct_letters"].append(letter)

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







