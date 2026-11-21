import random
WIDTH = 4
numList = [1,2,3,4,5,6,7,8,9,0]
############################################################
# functionality: randomly generate the target number
# input:
# numList: the list with 10 digits
# count: the number of digits to generate
# output: a list with four digits (integers)
def genNumbers(numList, count):
    random.shuffle(numList)
    numbers = numList[:count]
    return numbers
############################################################
############################################################
# functionality: obtain the guessing from users

# input: None
# output: a list with four digits (integers)
def userGuess():
    inputStr = input("Please input 4 digits: ")
    ## TODO ##
    ## Check user input and ensure user entered correct
    ## datatype and length of input.
    if len(inputStr) != 4 or not inputStr.isdigit():
        print("Invalid input. Please enter exactly 4 digits.")
        return userGuess()  # Prompt again for valid input

    guess = []
    for char in inputStr:
        guess.append(int(char))
    return guess
############################################################
############################################################
# functionality: compare the user guessing with the target
# input:
# guessList: the list of four digits (user guessing)
# answerList: the list of four digits (target)
# output: a tuple (#A, #B)
def checkGuess(guessList, answerList):
    ## TODO ##
    ## Check how many correct number entered by the user
    ## and return the count (bulls, cows).
    return (bulls, cows)
############################################################
############################################################
# Main program putting all function together
answer = genNumbers(numList, WIDTH)
#print(answer) ## UNCOMMENT THIS TO SEE WHAT WAS THE
## SHUFFLED LIST
attemps = 0
while True:
    guesses = userGuess()
    attemps += 1
    #print(guesses)
    result = checkGuess(guesses, answer)
    #print(result)
    if result[0] == 4:
        print("You Win!!")
        print("Attemps: ", attemps)
        break
    else:
        print(result[0], "A (Bulls)", result[1], "B (Cows)")