# Playfair Cipher Implementation
# Encryption and  Decryption

# Convert string to lowercase
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


# Generate 5x5 Playfair key table
def generateKeyTable(key):
    keyT = [['' for _ in range(5)] for _ in range(5)]

    used = [False] * 26

    # J and I are treated as the same character
    used[ord('j') - 97] = True

    i = 0
    j = 0

    # First insert characters from key
    for ch in key:
        if ch == 'j':
            ch = 'i'

        index = ord(ch) - 97

        if not used[index]:
            keyT[i][j] = ch
            used[index] = True

            j += 1

            if j == 5:
                j = 0
                i += 1

    # Then insert remaining alphabets
    for k in range(26):
        if not used[k]:
            keyT[i][j] = chr(k + 97)
            used[k] = True

            j += 1

            if j == 5:
                j = 0
                i += 1

            if i == 5:
                break

    return keyT


# Display key table
def displayKeyTable(keyT):
    print("\nKey Table:")

    for row in keyT:
        print(" ".join(row))


# Find position of a character
def findPosition(keyT, ch):
    if ch == 'j':
        ch = 'i'

    for i in range(5):
        for j in range(5):
            if keyT[i][j] == ch:
                return i, j

    return None, None


# Prepare plaintext into digraphs
def prepareText(text):
    result = ""

    i = 0

    while i < len(text):

        # Last character
        if i == len(text) - 1:
            result += text[i]
            result += 'z'
            break

        # Same characters in a pair
        if text[i] == text[i + 1]:
            result += text[i]
            result += 'z'
            i += 1

        else:
            result += text[i]
            result += text[i + 1]
            i += 2

    return result


# Encrypt a pair of characters
def encryptPair(a, b, keyT):

    r1, c1 = findPosition(keyT, a)
    r2, c2 = findPosition(keyT, b)

    # Same row
    if r1 == r2:
        a = keyT[r1][(c1 + 1) % 5]
        b = keyT[r2][(c2 + 1) % 5]

    # Same column
    elif c1 == c2:
        a = keyT[(r1 + 1) % 5][c1]
        b = keyT[(r2 + 1) % 5][c2]

    # Rectangle
    else:
        a = keyT[r1][c2]
        b = keyT[r2][c1]

    return a + b


# Encrypt plaintext
def encrypt(text, keyT):

    result = ""

    for i in range(0, len(text), 2):
        result += encryptPair(text[i], text[i + 1], keyT)

    return result


# Decrypt a pair of characters
def decryptPair(a, b, keyT):

    r1, c1 = findPosition(keyT, a)
    r2, c2 = findPosition(keyT, b)

    # Same row
    if r1 == r2:
        a = keyT[r1][(c1 - 1) % 5]
        b = keyT[r2][(c2 - 1) % 5]

    # Same column
    elif c1 == c2:
        a = keyT[(r1 - 1) % 5][c1]
        b = keyT[(r2 - 1) % 5][c2]

    # Rectangle
    else:
        a = keyT[r1][c2]
        b = keyT[r2][c1]

    return a + b


# Decrypt ciphertext
def decrypt(text, keyT):

    result = ""

    for i in range(0, len(text), 2):
        result += decryptPair(text[i], text[i + 1], keyT)

    return result


# Main program
key = input("Enter key: ")
plaintext = input("Enter plaintext: ")

# Convert to lowercase and remove spaces
key = toLowerCase(key)
plaintext = toLowerCase(plaintext)

key = removeSpaces(key)
plaintext = removeSpaces(plaintext)

# Replace j with i
key = key.replace('j', 'i')
plaintext = plaintext.replace('j', 'i')

# Generate key table
keyT = generateKeyTable(key)

# Display key table
displayKeyTable(keyT)

# Prepare plaintext
preparedText = prepareText(plaintext)

print("\nPrepared Plaintext:", preparedText)

# Encryption
ciphertext = encrypt(preparedText, keyT)

print("Ciphertext:", ciphertext)

# Decryption
decryptedText = decrypt(ciphertext, keyT)

print("Decrypted Text:", decryptedText)