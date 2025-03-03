import os
import sys

def getExtension():
    filename = input("Please enter a filename: ")
    root, ext = os.path.splitext(filename)

    if not ext:
        raise ValueError("The file does not have an extension")
    
    return ext

if __name__ == "__main__":
    ext = getExtension()
    print(f"Extension is {ext}")