
DEFAULT_PLAINTEXT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
DEFAULT_CIPHER_ALPHABET = "defghijklmnopqrstuvwxyzabc"
DEFAULT_ENCRYPTION_MAP = {
    "a": "d",
    "b": "e",
    "c": "f",
    "d": "g",
    "e": "h",
    "f": "i",
    "g": "j",
    "h": "k",
    "i": "l",
    "j": "m",
    "k": "n",
    "l": "o",
    "m": "p",
    "n": "q",
    "o": "r",
    "p": "s",
    "q": "t",
    "r": "u",
    "s": "v",
    "t": "w",
    "u": "x",
    "v": "y",
    "w": "z",
    "x": "a",
    "y": "b",
    "z": "c",
}
DEFAULT_DECRYPTION_MAP = {value: key for key, value in DEFAULT_ENCRYPTION_MAP.items()}


def validate_alphabets(plaintext_alphabet: str, cipher_alphabet: str) -> None:
    if len(plaintext_alphabet) != len(cipher_alphabet):
        raise ValueError("Plaintext and cipher alphabets must have the same length.")
    if len(set(plaintext_alphabet)) != len(plaintext_alphabet):
        raise ValueError("Plaintext alphabet contains duplicate characters.")
    if len(set(cipher_alphabet)) != len(cipher_alphabet):
        raise ValueError("Cipher alphabet contains duplicate characters.")


def substitute_text(text: str, mapping: dict) -> str:
    result = []
    for ch in text:
        if ch.lower() in mapping:
            mapped = mapping[ch.lower()]
            result.append(mapped.upper() if ch.isupper() else mapped)
        else:
            result.append(ch)
    return "".join(result)


def encrypt(message: str, plaintext_alphabet: str = DEFAULT_PLAINTEXT_ALPHABET, cipher_alphabet: str = DEFAULT_CIPHER_ALPHABET) -> str:
    """Encrypt a message using monoalphabetic substitution."""
    if plaintext_alphabet == DEFAULT_PLAINTEXT_ALPHABET and cipher_alphabet == DEFAULT_CIPHER_ALPHABET:
        return substitute_text(message, DEFAULT_ENCRYPTION_MAP)

    validate_alphabets(plaintext_alphabet, cipher_alphabet)
    mapping = {from_char: to_char for from_char, to_char in zip(plaintext_alphabet, cipher_alphabet)}
    return substitute_text(message, mapping)


def decrypt(cipher_text: str, plaintext_alphabet: str = DEFAULT_PLAINTEXT_ALPHABET, cipher_alphabet: str = DEFAULT_CIPHER_ALPHABET) -> str:
    """Decrypt a message using monoalphabetic substitution."""
    if plaintext_alphabet == DEFAULT_PLAINTEXT_ALPHABET and cipher_alphabet == DEFAULT_CIPHER_ALPHABET:
        return substitute_text(cipher_text, DEFAULT_DECRYPTION_MAP)

    validate_alphabets(plaintext_alphabet, cipher_alphabet)
    reverse_mapping = {to_char: from_char for from_char, to_char in zip(plaintext_alphabet, cipher_alphabet)}
    return substitute_text(cipher_text, reverse_mapping)


if __name__ == "__main__":
    sample_message = "Hello Bhai 123!"
    encrypted = encrypt(sample_message)
    decrypted = decrypt(encrypted)

    print("Plaintext:", sample_message)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
                    
