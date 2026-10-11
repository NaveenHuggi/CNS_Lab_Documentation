alphabets = "abcdefghijklmnopqrstuvwxyz"
k = 3
keyword  = "hello"

def substitution_cypher(alphabets, k, keyword):
    message = []

    for ch in keyword:
        pos = 0
        for index,val in enumerate(alphabets):
            if(ch == val):
                pos = index
        message.append(alphabets[(k + pos) % 26])


    return message

def decrypt_message(alphabets, k, decrypt_message):
    original = []

    for ch in decrypt_message:
        for index,val in enumerate(alphabets):
                if(ch == val):
                    pos = index

        original.append(alphabets[(pos - k) % 26])

    return original

decrypted_message = substitution_cypher(alphabets, k, keyword)

original_message = decrypt_message(alphabets, k, decrypted_message)

print(decrypted_message)
print(original_message)


