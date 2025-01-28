import sys

if __name__ == "__main__":
    input_string = input("Please enter a list of integers separated using commas: ")
    numbers = list(map(int, input_string.split(",")))

    numbers_set = set(numbers)
    print(f"Removed duplicates: {numbers_set}")

    numbers_tuple = tuple(numbers)
    print(f"Tuple: {numbers_tuple}")

    min = min(numbers_set)
    max = max(numbers_set)
    print(f"Min number is: {min} and max is: {max}")
    