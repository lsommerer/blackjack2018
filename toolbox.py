#
# These are procedures that I'm going to use over and over again.
#

def get_integer(prompt):
    """Asks the user the prompt and verifies they enter an integer"""
    #
    # If there's no space at the end of prompt, add one.
    #
    if prompt[-1] != " ":
        prompt = prompt + " "
    number = input(prompt)
    #
    # We're only going to use prompt again if they entered something that
    # is not an integer, so it's simpler just to change the prompt once
    # outside the loop.
    #
    prompt = prompt + "(integers only) "
    #
    # If they didn't enter an integer, ask them to enter one.
    #
    while not is_integer(number):
        number = input(prompt)
    number = int(number)
    return number


def is_integer(number):
    """Returns True is number is an interger else it returns False."""
    isInteger = True
    #
    # Remove leading and trailing whites space and
    # check for 4 special cases of non-integers. Then
    # remove any leading positive or negative signs.
    #
    number = str(number).strip()
    if number in ['', '.', '+', '-']:
        isInteger = False
    if isInteger and number[0] in '+-':
        number = number[1:]
        #
    # Loop through the string checking to make sure
    # the characters are all legal integer characters.
    #
    position = 0
    legalValues = '0123456789.'
    while isInteger and position <= len(number) - 1:
        if number[position] not in legalValues:
            isInteger = False
        if number[position] == '.':
            legalValues = '0'
        position += 1

    return isInteger


def get_number(prompt):
    """Asks the user the prompt and verifies they enter a float"""
    if prompt[-1] != " ":
        prompt += " "
    number = input(prompt)
    while not is_number(number):
        if prompt[-16:] != " (numbers only) ":
            prompt = prompt + "(numbers only) "
        number = input(prompt)
    number = float(number)
    return number


def is_number(number):
    '''Returns True is testValue is a number, otherwise returns False.'''
    isNumber = True
    testValue = str(number)
    isNumber = True
    #
    # Remove leading and trailing whites space and
    # check for 4 special cases of non-numbers. Then
    # remove any leading positive or negative signs.
    #
    number = str(number).strip()
    if number in ['', '.', '+', '-']:
        isNumber = False
    if isNumber and number[0] in '+-':
        number = number[1:]
        #
    # Loop through the string checking to make sure
    # the characters are all legal integer characters.
    #
    legalValues = '.0123456789'
    for character in number:
        if character not in legalValues:
            isNumber = False
        if character == '.':
            legalValues = '0123456789'

    return isNumber


def get_positive_number(prompt):
    """returns a positive number."""
    number = get_number(prompt)
    while number < 0:
        print("You have to enter a positive value.")
        number = get_number(prompt)
    return number


def get_integer_between(low, high, prompt="Enter an integer:"):
    prompt += " (" + str(low) + "-" + str(high) + ")"
    number = get_integer(prompt)
    while (number < low) or (number > high):
        number = get_integer(prompt)
    return number


def get_number_between(low, high, prompt="Enter a number:"):
    number = get_number(prompt)
    prompt += " (" + str(low) + "-" + str(high) + ")"
    while (number < low) or (number > high):
        number = get_number(prompt)
    return number


def get_boolean(prompt):
    """Ask the user a yes or no question"""
    prompt = prompt + " (y/n) "
    answer = input(prompt)
    answer = answer.lower()
    if answer in ['yes', 'sure', 'yeah', 'true', 'absolutely', 'y', 'da', 'si']:
        answer = True
    elif answer in ['n', 'no', 'nope', 'nah']:
        answer = False
    else:
        prompt = "Does " + answer + " mean yes or no?"
        answer = get_boolean(prompt)
    return answer


def get_string(prompt):
    """Get and return a non-empty string"""
    if prompt[-1] != " ":
        prompt = prompt + " "
    string = input(prompt)
    while not string:
        if prompt[-31:] != " (you have to enter something) ":
            prompt = prompt + "(you have to enter something) "
        string = input(prompt)
    return string


def print_separator(character, length=60):
    """Prints length number of characters."""
    string = (character[0] * int(length))
    print(string)


def print_centered(string, length=60, character=" "):
    """Prints a string centered on a line of length length."""
    stringLength = len(string)
    padding = int((length - stringLength) / 2)
    if padding > 0:
        centeredString = character[0] * padding + string + character[0] * padding
    else:
        centeredString = string[:length]
    print(centeredString)


def yes_or_no(prompt):
    """This allows my older code to work."""
    return get_boolean(prompt)


