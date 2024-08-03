import re
import random
import configparser

# Function to read words from a text file into a list
def read_file(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    return words


# regex for letters that must be included
def correct_expression(guess_param):
    correct_regex = ""
    for correct_letter in guess_param["correct_letters"]:
        correct_regex += f"(?=.*{correct_letter})"
    return correct_regex
        

# filter the list of words based on regex pattern from guess param
def generate_list(guess_param, word_list):
    include_letters = correct_expression(guess_param)
    exclude_letters = guess_param["excluded_letters"]
    correct_letters = ""
    search_expression = f"{include_letters}"
    # counters for consecutive correct letters
    counter2 = 0
    # index of the first correct letter
    position2 = 0

    for index, position in enumerate(guess_param["correct_positions"]):
        if position == "0":
            if guess_param["wrong_position"][index] != "":
                exclude_expression = exclude_letters + guess_param["wrong_position"][index]
            else:
                exclude_expression = exclude_letters
            search_expression += f"[^{exclude_expression}]{{1}}"
        else:
            search_expression += guess_param["correct_positions"][index]
    search_expression += "$"

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

        elif result == "1":
            print("Correct letter but wrong position")
            if letter not in guess_param["correct_letters"] and letter not in guess_param["correct_positions"]:
                guess_param["correct_letters"].append(letter)
            if letter not in guess_param["wrong_position"][index]:
                guess_param["wrong_position"][index] += letter

        else:
            print("Wrong letter")
            if letter not in guess_param["excluded_letters"] and letter not in guess_param["correct_letters"]:
                guess_param["excluded_letters"] += letter
    print(guess_param)


config = configparser.ConfigParser()
config.read('config.ini')
file_path = config['DEFAULT']['LIST_FILE_PATH']
word_list = read_file(file_path)
dictionary_size = len(word_list)
print(f"valid word list: {dictionary_size}")
random_index = random.randint(0, dictionary_size - 1)
guess = word_list[random_index]
print(guess)

guess_param = {
    "guess": guess,
    "excluded_letters": "",
    "correct_letters": [],
    "wrong_position" : ["", "", "", "", ""],
    "correct_positions": ["0","0","0","0","0"]
}

feedback = 00000
while feedback != 22222:
    print("Input 2 for correct letter and position, 1 for correct letter and wrong position, 0 for wrong letter: ")
    feedback = input(": ")
    if feedback == "22222":
        break
    update_parameters(guess_param, feedback)
    word_list = generate_list(guess_param, word_list)
    random_index = random.randint(0, len(word_list) - 1)
    guess = word_list[random_index]
    guess_param["guess"] = guess
    print(guess)
print("Game Won!")






