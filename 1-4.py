if __name__ == "__main__":

    input_string = input("Please enter a string: ")

    characters = {}

    for c in input_string:
        if c in characters:
            characters[c] += 1
        else:
            characters[c] = 1

    print(characters)
