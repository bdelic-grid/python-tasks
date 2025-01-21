import os
import sys

def getException():
    filename = input("Please enter a filename: ")
    root, ext = os.path.splitext(filename)

    if not ext:
        raise ValueError("The file does not have an extension")
    
    return ext

if __name__ == "__main__":
    try:
        ext = getException()
        print(f"Extension is {ext}")
    except ValueError as e:
        print(e)
        sys.exit(1)