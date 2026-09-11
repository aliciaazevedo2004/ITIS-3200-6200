import hashlib
import os
import json

#Calculates hash of file content
def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

#Navigates to directory entered by user
def traverse_directory(directory):
    hashes = {}

    for root, directories, files in os.walk(directory):
        

        for filename in files:
            filepath = os.path.join(root, filename)
            hashes[filepath]=hash_file(filepath)
    return hashes

#Makes hash table with given information
def generate_table():
    directory = input("Please enter desired directory path: ")
    hashes = traverse_directory(directory)
    with open("hash_table.json", "w") as file:
        json.dump(hashes, file, indent=4)
    print("Hash table has been generated")

#Returns validity messages based on status of files
def validate_hash():
    with open("hash_table.json", "r") as file:
        stored_hashes = json.load(file)

    directory = input("Please enter a directory path: ")

    current_hashes = traverse_directory(directory)

    for filepath, stored_hash in stored_hashes.items():
        if filepath not in current_hashes:
            print(filepath + " has been deleted")
        else:
            current_hash = current_hashes[filepath]

            if current_hash == stored_hash:
                print(filepath + " hash is valid")
            else:
                print(filepath + " hash is invalid")

    for filepath in current_hashes:
        if filepath not in stored_hashes:
            print(filepath + " is a new file")

def main():
    print("1. Generate new hash table")
    print("2. Verify hashes")

    choices = input("Please enter one of the choices: ")

    if choices == "1":
        generate_table()
    elif choices == "2":
        validate_hash()
    else:
        print("Choice is invalid. Please enter 1 or 2.")

main()
