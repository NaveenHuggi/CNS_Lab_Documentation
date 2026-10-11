# Hill Cipher Implementation
# Encryption and  Decryption

import math


# Convert text to lowercase
def toLowerCase(text):
    result = ""

    for ch in text:
        if 'A' <= ch <= 'Z':
            result += chr(ord(ch) + 32)
        else:
            result += ch

    return result


# Remove spaces
def removeSpaces(text):
    result = ""

    for ch in text:
        if ch != ' ':
            result += ch

    return result


# Convert character to number
# a = 0, b = 1, ..., z = 25
def charToNum(ch):
    return ord(ch) - ord('a')


# Convert number to character
def numToChar(num):
    return chr((num % 26) + ord('a'))


# Find modular inverse
def modInverse(a, m):

    a = a % m

    for x in range(1, m):
        if (a * x) % m == 1:
            return x

    return None


# Find inverse of 2x2 matrix
def inverseMatrix(key):

    a = key[0][0]
    b = key[0][1]
    c = key[1][0]
    d = key[1][1]

    # Determinant
    determinant = (a * d) - (b * c)

    determinant = determinant % 26

    # Modular inverse of determinant
    determinantInverse = modInverse(determinant, 26)

    if determinantInverse is None:
        print("Inverse does not exist!")
        return None

    # Adjugate matrix
    inverse = [
        [d, -b],
        [-c, a]
    ]

    # Multiply by determinant inverse
    for i in range(2):
        for j in range(2):
            inverse[i][j] = (
                inverse[i][j] * determinantInverse
            ) % 26

    return inverse


# Prepare plaintext
def prepareText(text):

    # Hill cipher with 2x2 matrix
    # requires even length

    if len(text) % 2 != 0:
        text += 'x'

    return text


# Encrypt plaintext
def encrypt(text, key):

    result = ""

    for i in range(0, len(text), 2):

        # Convert pair to numbers
        x1 = charToNum(text[i])
        x2 = charToNum(text[i + 1])

        # Matrix multiplication
        y1 = (key[0][0] * x1 +
              key[0][1] * x2) % 26

        y2 = (key[1][0] * x1 +
              key[1][1] * x2) % 26

        result += numToChar(y1)
        result += numToChar(y2)

    return result


# Decrypt ciphertext
def decrypt(text, inverseKey):

    result = ""

    for i in range(0, len(text), 2):

        # Convert pair to numbers
        y1 = charToNum(text[i])
        y2 = charToNum(text[i + 1])

        # Matrix multiplication
        x1 = (inverseKey[0][0] * y1 +
              inverseKey[0][1] * y2) % 26

        x2 = (inverseKey[1][0] * y1 +
              inverseKey[1][1] * y2) % 26

        result += numToChar(x1)
        result += numToChar(x2)

    return result


# Display matrix
def displayMatrix(matrix):

    for row in matrix:
        print(row)


# Main program

print("===== HILL CIPHER =====")

# Input key matrix
print("\nEnter 2x2 key matrix:")

key = []

for i in range(2):
    row = list(map(int, input(
        f"Enter row {i + 1} (2 numbers): "
    ).split()))

    key.append(row)


# Input plaintext
plaintext = input("\nEnter plaintext: ")


# Preprocessing
plaintext = toLowerCase(plaintext)
plaintext = removeSpaces(plaintext)


# Prepare plaintext
plaintext = prepareText(plaintext)


print("\nKey Matrix:")
displayMatrix(key)

print("\nPrepared Plaintext:", plaintext)


# Find inverse matrix
inverseKey = inverseMatrix(key)

if inverseKey is None:
    print("Choose another key matrix.")
else:

    print("\nInverse Key Matrix:")
    displayMatrix(inverseKey)

    # Encryption
    ciphertext = encrypt(plaintext, key)

    print("\nCiphertext:", ciphertext)

    # Decryption
    decryptedText = decrypt(ciphertext, inverseKey)

    print("Decrypted Text:", decryptedText)