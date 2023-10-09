WORD = "DROOL"

guess = "FROOL"
if guess == WORD:
    print("Correct")


correct_letters = {
    letter for letter, correct in zip(guess, WORD) if letter == correct
}
misplaced_letters = set(guess) & set(WORD) - correct_letters
wrong_letters = set(guess) - set(WORD)

print(f"Correct letters: {correct_letters}")
print(f"Misplaced letters: {misplaced_letters}")
print(f"Wrong letters: {wrong_letters}")

# transfor to list
wrong_letters_list = []
correct_letters_list = []
misplaced_letters_list = []

# Convert sets to lists
word_list = list(WORD)
guess_list = list(guess)
print(guess_list)
for index, letter_g in enumerate(guess_list):
    # Make initial append
    misplaced_letters_list.append('_')
    # Iterrate through the misplaced set
    for letter_m in misplaced_letters.copy():
        if letter_m == guess_list[index]:
            print(f"Yes {letter_m} matched so adding to misplaced list")
            misplaced_letters_list[index] = letter_m
            misplaced_letters.remove(letter_m)
        
for index, letter_g in enumerate(guess_list):
    # Make initial append
    correct_letters_list.append('_')
    # Iterrate through the misplaced set
    for letter_c in correct_letters.copy():
        if letter_c == guess_list[index]:
            print(f"Yes {letter_c} matched so adding to correct list")
            correct_letters_list[index] = letter_c
            correct_letters.remove(letter_c)

for index, letter_g in enumerate(guess_list):
    # Make initial append
    wrong_letters_list.append('_')
    # Iterrate through the misplaced set
    for letter_w in wrong_letters.copy():
        if letter_w == guess_list[index]:
            print(f"Yes {letter_w} matched so adding to correct list")
            wrong_letters_list[index] = letter_w
            wrong_letters.remove(letter_w)

print(f"Green:  {correct_letters_list}")
print(f"Yellow: {misplaced_letters_list}")
print(f"Grey:   {wrong_letters_list}")
