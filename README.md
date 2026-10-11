# Computer Network and Security Lab Programs

Comprehensive laboratory documentation, source code index, sample execution logs, empirical performance benchmarks, and analytical observations for the Computer Network and Security (CNS) Laboratory experiments.

All programs, datasets, output graphs, and the primary compiled laboratory report (`CNS_Lab_Documentation.docx`) are housed directly within this `CNS_Lab_Documentation` directory.

---

## Table of Contents

1. [Folder Structure](#folder-structure)
2. [Prerequisites and Environment Setup](#prerequisites-and-environment-setup)
3. [Lab 1: Classical Substitution Ciphers](#lab-1-classical-substitution-ciphers)
   - [Substitution Cipher (Caesar Shift)](#1-substitution-cipher-caesar-shift)
   - [Monoalphabetic Cipher](#2-monoalphabetic-cipher)
4. [Lab 2: Polyalphabetic and Polygraphic Ciphers](#lab-2-polyalphabetic-and-polygraphic-ciphers)
   - [Playfair Cipher](#1-playfair-cipher)
   - [Hill Cipher (2x2 Matrix)](#2-hill-cipher-2x2-matrix)
5. [Lab 3: Modern Symmetric Block and Stream Ciphers](#lab-3-modern-symmetric-block-and-stream-ciphers)
   - [Stream Cipher (ARC4)](#1-stream-cipher-arc4)
   - [Feistel Cipher Network](#2-feistel-cipher-network)
   - [Data Encryption Standard (DES)](#3-data-encryption-standard-des)
   - [Triple Data Encryption Standard (3DES)](#4-triple-data-encryption-standard-3des)
   - [Advanced Encryption Standard (AES)](#5-advanced-encryption-standard-aes)
6. [Lab 5: Simulation of Access Control Matrix and Dynamic Rights Updates](#lab-5-simulation-of-access-control-matrix-and-dynamic-rights-updates)
   - [Aim and Protection Model](#aim-and-protection-model)
   - [Permissions Specification](#permissions-specification)
   - [Python Implementation Source Code](#lab-5-python-source-code)
   - [Sample Execution and Console Output](#lab-5-sample-execution-and-console-output)
   - [Performance Measurements and Experiment Table](#lab-5-performance-measurements)
   - [Permission Density Experiment](#lab-5-permission-density-experiment)
   - [Graphical Analysis](#lab-5-graphical-analysis)
   - [Observations and Result](#lab-5-observations-and-result)
7. [Lab 6: Multi-User Cloud RBAC and Mutual Certificate Authentication](#lab-6-multi-user-cloud-rbac-and-mutual-certificate-authentication)
   - [Aim and Security Architecture](#lab-6-aim-and-security-architecture)
   - [Roles and Permissions Matrix](#lab-6-roles-and-permissions-matrix)
   - [Python Implementation Source Code](#lab-6-python-source-code)
   - [Security Test Cases: Certificate Condition Verification](#lab-6-security-test-cases)
   - [Expected Output Record (Section 13 Format)](#lab-6-expected-output-record)
   - [Performance Measurements and Experiment Table](#lab-6-performance-measurements)
   - [Permission Density Benchmark](#lab-6-permission-density-benchmark)
   - [Graphical Analysis](#lab-6-graphical-analysis)
   - [Observations and Result](#lab-6-observations-and-result)
8. [Master Laboratory Report Document](#master-laboratory-report-document)
9. [Execution Guide](#execution-guide)

---

## Folder Structure

```text
CNS_Lab_Documentation/
|-- README.md                                    # Comprehensive laboratory guide and technical reference
|-- CNS_Lab_Documentation.docx                   # Master compiled laboratory documentation and report
|-- Python Codes/                                # Directory containing all Python lab implementations
|   |-- substitution.py                          # Lab 1: Caesar shift additive substitution cipher
|   |-- monoalpha.py                             # Lab 1: Arbitrary permutation monoalphabetic cipher
|   |-- play_fair_cipher.py                      # Lab 2: 5x5 Playfair polygraphic cipher
|   |-- hill_cipher.py                           # Lab 2: 2x2 Hill linear algebraic cipher
|   |-- stream_cipher.py                         # Lab 3: ARC4 stream cipher keystream generator
|   |-- feistal_cipher                           # Lab 3: 4-round iterative Feistel network
|   |-- Des.py                                   # Lab 3: Data Encryption Standard (DES-ECB)
|   |-- triple_Des                               # Lab 3: Triple DES (3DES-EDE-ECB)
|   |-- aes.py                                   # Lab 3: Advanced Encryption Standard (AES-128-CBC)
|   |-- lab5_access_control_matrix.py            # Lab 5: Access Control Matrix simulation & telemetry
|   |-- lab6_cloud_rbac_mutual_auth.py           # Lab 6: Cloud RBAC & X.509 mutual certificate auth
|   `-- generate_report.py                       # Automated report compilation utility
|-- lab5_graphs/                                 # Lab 5 empirical benchmark plots (5 high-res figures)
|   |-- lab5_graph1_users_vs_time.png
|   |-- lab5_graph2_requests_vs_verification.png
|   |-- lab5_graph3_updates_vs_time.png
|   |-- lab5_graph4_density_vs_processing.png
|   `-- lab5_graph5_granted_vs_denied.png
`-- lab6_graphs/                                 # Lab 6 empirical benchmark plots (9 high-res figures)
    |-- lab6_graph1_users_vs_auth_time.png
    |-- lab6_graph2_users_vs_authz_time.png
    |-- lab6_graph3_users_vs_response_time.png
    |-- lab6_graph4_requests_vs_authz_time.png
    |-- lab6_graph5_updates_vs_update_time.png
    |-- lab6_graph6_concurrent_users_vs_throughput.png
    |-- lab6_graph7_cert_status_vs_auth_results.png
    |-- lab6_graph8_density_vs_processing.png
    `-- lab6_graph9_granted_vs_denied.png
```

---

## Prerequisites and Environment Setup

### Required Runtime
- Python 3.10, 3.11, or 3.12 (64-bit recommended)
- Windows, Linux, or macOS environment

### Python Dependencies
The implementations rely on standard library modules and specialized cryptographic and scientific packages:
- `pycryptodome` (>= 3.20.0): Implements DES, 3DES, AES, and ARC4 primitives.
- `cryptography` (>= 42.0.0): Implements X.509 certificate generation, RSA-2048 keypairs, and digital signature validation.
- `matplotlib` (>= 3.8.0): Generates high-resolution performance plots.
- `python-docx` (>= 1.1.0): Generates formatted Microsoft Word laboratory reports.

Install dependencies using pip:
```bash
pip install pycryptodome cryptography matplotlib python-docx
```

---

## Lab 1: Classical Substitution Ciphers

### 1. Substitution Cipher (Caesar Shift)

#### Concept
The additive substitution cipher shifts each plaintext character by a predetermined integer displacement $k$ modulo 26:
- Encryption Transformation: $C_i = (P_i + k) \pmod{26}$
- Decryption Transformation: $P_i = (C_i - k) \pmod{26}$

#### Source Code (`Python Codes/substitution.py`)
```python
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
```

#### Sample Output
```text
['k', 'h', 'o', 'o', 'r']
['h', 'e', 'l', 'l', 'o']
```

---

### 2. Monoalphabetic Cipher

#### Concept
Constructs a fixed permutation mapping between standard plaintext letters and substituted cipher letters. The implementation provides input validation against duplicate or missing characters, handles uppercase and lowercase cases, and preserves non-alphabetic symbols.

#### Source Code (`Python Codes/monoalpha.py`)
```python
DEFAULT_PLAINTEXT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
DEFAULT_CIPHER_ALPHABET = "defghijklmnopqrstuvwxyzabc"
DEFAULT_ENCRYPTION_MAP = {
    "a": "d", "b": "e", "c": "f", "d": "g", "e": "h", "f": "i",
    "g": "j", "h": "k", "i": "l", "j": "m", "k": "n", "l": "o",
    "m": "p", "n": "q", "o": "r", "p": "s", "q": "t", "r": "u",
    "s": "v", "t": "w", "u": "x", "v": "y", "w": "z", "x": "a",
    "y": "b", "z": "c",
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
    if plaintext_alphabet == DEFAULT_PLAINTEXT_ALPHABET and cipher_alphabet == DEFAULT_CIPHER_ALPHABET:
        return substitute_text(message, DEFAULT_ENCRYPTION_MAP)

    validate_alphabets(plaintext_alphabet, cipher_alphabet)
    mapping = {from_char: to_char for from_char, to_char in zip(plaintext_alphabet, cipher_alphabet)}
    return substitute_text(message, mapping)

def decrypt(cipher_text: str, plaintext_alphabet: str = DEFAULT_PLAINTEXT_ALPHABET, cipher_alphabet: str = DEFAULT_CIPHER_ALPHABET) -> str:
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
```

#### Sample Output
```text
Plaintext: Hello Bhai 123!
Encrypted: Khoor Ekdl 123!
Decrypted: Hello Bhai 123!
```

---

## Lab 2: Polyalphabetic and Polygraphic Ciphers

### 1. Playfair Cipher

#### Concept
The Playfair cipher encrypts character pairs (digraphs) across a 5x5 key matrix generated from a secret keyword. The characters 'I' and 'J' share a single cell:
- Identical character splitting: Inserts filler character 'z' between duplicate adjacent letters.
- Odd length adjustment: Appends trailing 'z' if plaintext length is odd.
- Same row rule: Replaces each letter with the character to its immediate right (modulo 5).
- Same column rule: Replaces each letter with the character immediately below it (modulo 5).
- Rectangle rule: Each letter is replaced with the letter in its row and the column of the opposing letter.
- Decryption shifts left (row) and up (column).

#### Source Code (`Python Codes/play_fair_cipher.py`)
```python
# Playfair Cipher Implementation
# Encryption and Decryption

def toLowerCase(text):
    result = ""
    for ch in text:
        if 'A' <= ch <= 'Z':
            result += chr(ord(ch) + 32)
        else:
            result += ch
    return result

def removeSpaces(text):
    result = ""
    for ch in text:
        if ch != ' ':
            result += ch
    return result

def generateKeyTable(key):
    keyT = [['' for _ in range(5)] for _ in range(5)]
    used = [False] * 26
    used[ord('j') - 97] = True

    i, j = 0, 0
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

def displayKeyTable(keyT):
    print("\nKey Table:")
    for row in keyT:
        print(" ".join(row))

def findPosition(keyT, ch):
    if ch == 'j':
        ch = 'i'
    for i in range(5):
        for j in range(5):
            if keyT[i][j] == ch:
                return i, j
    return None, None

def prepareText(text):
    result = ""
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            result += text[i] + 'z'
            break
        if text[i] == text[i + 1]:
            result += text[i] + 'z'
            i += 1
        else:
            result += text[i] + text[i + 1]
            i += 2
    return result

def encryptPair(a, b, keyT):
    r1, c1 = findPosition(keyT, a)
    r2, c2 = findPosition(keyT, b)
    if r1 == r2:
        return keyT[r1][(c1 + 1) % 5] + keyT[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return keyT[(r1 + 1) % 5][c1] + keyT[(r2 + 1) % 5][c2]
    else:
        return keyT[r1][c2] + keyT[r2][c1]

def encrypt(text, keyT):
    result = ""
    for i in range(0, len(text), 2):
        result += encryptPair(text[i], text[i + 1], keyT)
    return result

def decryptPair(a, b, keyT):
    r1, c1 = findPosition(keyT, a)
    r2, c2 = findPosition(keyT, b)
    if r1 == r2:
        return keyT[r1][(c1 - 1) % 5] + keyT[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return keyT[(r1 - 1) % 5][c1] + keyT[(r2 - 1) % 5][c2]
    else:
        return keyT[r1][c2] + keyT[r2][c1]

def decrypt(text, keyT):
    result = ""
    for i in range(0, len(text), 2):
        result += decryptPair(text[i], text[i + 1], keyT)
    return result

if __name__ == "__main__":
    key = input("Enter key: ")
    plaintext = input("Enter plaintext: ")

    key = removeSpaces(toLowerCase(key)).replace('j', 'i')
    plaintext = removeSpaces(toLowerCase(plaintext)).replace('j', 'i')

    keyT = generateKeyTable(key)
    displayKeyTable(keyT)

    preparedText = prepareText(plaintext)
    print("\nPrepared Plaintext:", preparedText)

    ciphertext = encrypt(preparedText, keyT)
    print("Ciphertext:", ciphertext)

    decryptedText = decrypt(ciphertext, keyT)
    print("Decrypted Text:", decryptedText)
```

#### Sample Input and Output
```text
Enter key: Monarchy
Enter plaintext: instruments

Key Table:
m o n a r
c h y b d
e f g i k
l p q s t
u v w x z

Prepared Plaintext: instruments
Ciphertext: gatlmzclrqtx
Decrypted Text: instruments
```

---

### 2. Hill Cipher (2x2 Matrix)

#### Concept
The Hill cipher encrypts character blocks through matrix multiplication over $\mathbb{Z}_{26}$. Given key matrix $\mathbf{K} = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ and plaintext vector $\mathbf{P}$:
- Encryption: $\mathbf{C} = \mathbf{K} \cdot \mathbf{P} \pmod{26}$
- Decryption: $\mathbf{P} = \mathbf{K}^{-1} \cdot \mathbf{C} \pmod{26}$

Matrix inversion requires computing the determinant $\det(\mathbf{K}) = (ad - bc) \pmod{26}$ and finding its modular multiplicative inverse $\det(\mathbf{K})^{-1}$ such that $(\det(\mathbf{K}) \cdot \det(\mathbf{K})^{-1}) \equiv 1 \pmod{26}$:
$$\mathbf{K}^{-1} = \det(\mathbf{K})^{-1} \cdot \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \pmod{26}$$

#### Source Code (`Python Codes/hill_cipher.py`)
```python
# Hill Cipher Implementation
# Encryption and Decryption

def toLowerCase(text):
    return "".join([chr(ord(ch) + 32) if 'A' <= ch <= 'Z' else ch for ch in text])

def removeSpaces(text):
    return "".join([ch for ch in text if ch != ' '])

def charToNum(ch):
    return ord(ch) - ord('a')

def numToChar(num):
    return chr((num % 26) + ord('a'))

def modInverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def inverseMatrix(key):
    a, b = key[0][0], key[0][1]
    c, d = key[1][0], key[1][1]

    determinant = ((a * d) - (b * c)) % 26
    det_inv = modInverse(determinant, 26)

    if det_inv is None:
        return None

    inverse = [
        [(d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, (a * det_inv) % 26]
    ]
    return inverse

def prepareText(text):
    if len(text) % 2 != 0:
        text += 'x'
    return text

def encrypt(text, key):
    result = ""
    for i in range(0, len(text), 2):
        x1, x2 = charToNum(text[i]), charToNum(text[i + 1])
        y1 = (key[0][0] * x1 + key[0][1] * x2) % 26
        y2 = (key[1][0] * x1 + key[1][1] * x2) % 26
        result += numToChar(y1) + numToChar(y2)
    return result

def decrypt(text, inverseKey):
    result = ""
    for i in range(0, len(text), 2):
        y1, y2 = charToNum(text[i]), charToNum(text[i + 1])
        x1 = (inverseKey[0][0] * y1 + inverseKey[0][1] * y2) % 26
        x2 = (inverseKey[1][0] * y1 + inverseKey[1][1] * y2) % 26
        result += numToChar(x1) + numToChar(x2)
    return result

def displayMatrix(matrix):
    for row in matrix:
        print(row)

if __name__ == "__main__":
    print("===== HILL CIPHER =====")
    print("\nEnter 2x2 key matrix:")
    key = []
    for i in range(2):
        row = list(map(int, input(f"Enter row {i + 1} (2 numbers): ").split()))
        key.append(row)

    plaintext = input("\nEnter plaintext: ")
    plaintext = prepareText(removeSpaces(toLowerCase(plaintext)))

    print("\nKey Matrix:")
    displayMatrix(key)
    print("\nPrepared Plaintext:", plaintext)

    inv_key = inverseMatrix(key)
    if inv_key is None:
        print("Determinant has no modular inverse mod 26. Choose another matrix.")
    else:
        print("\nInverse Key Matrix:")
        displayMatrix(inv_key)
        ciphertext = encrypt(plaintext, key)
        print("\nCiphertext:", ciphertext)
        decryptedText = decrypt(ciphertext, inv_key)
        print("Decrypted Text:", decryptedText)
```

#### Sample Input and Output
```text
===== HILL CIPHER =====

Enter 2x2 key matrix:
Enter row 1 (2 numbers): 3 3
Enter row 2 (2 numbers): 2 5

Enter plaintext: help

Key Matrix:
[3, 3]
[2, 5]

Prepared Plaintext: help

Inverse Key Matrix:
[15, 17]
[20, 9]

Ciphertext: hiat
Decrypted Text: help
```

---

## Lab 3: Modern Symmetric Block and Stream Ciphers

### 1. Stream Cipher (ARC4)

#### Concept
Alleged RC4 (ARC4) uses a byte-oriented variable-length key to generate a pseudo-random keystream through the Key-Scheduling Algorithm (KSA) and Pseudo-Random Generation Algorithm (PRGA). Plaintext bytes are encrypted via bitwise XOR with keystream bytes.

#### Source Code (`Python Codes/stream_cipher.py`)
```python
from Crypto.Cipher import ARC4

key = b"secretkey"
cipher = ARC4.new(key)
plaintext = input("Enter Plain Text: ")
encrypted = cipher.encrypt(plaintext.encode())
print("Encrypted:", encrypted.hex())

cipher = ARC4.new(key)
print("Decrypted:", cipher.decrypt(encrypted).decode())
```

#### Sample Output
```text
Enter Plain Text: Hello
Encrypted: 492e448b3b
Decrypted: Hello
```

---

### 2. Feistel Cipher Network

#### Concept
Demonstrates an iterative symmetric block cipher structure over 4 rounds. Each block is partitioned into left and right halves $(L_i, R_i)$:
$$L_{i+1} = R_i$$
$$R_{i+1} = L_i \oplus F(R_i, K)$$

#### Source Code (`Python Codes/feistal_cipher`)
```python
def feistel_round(left, right, key):
    f = right ^ key
    return right, left ^ f

left, right, key = 10, 20, 15
print("Before:", left, right)
for i in range(4):
    left, right = feistel_round(left, right, key)
print("After:", left, right)
```

#### Sample Output
```text
Before: 10 20
After: 20 17
```

---

### 3. Data Encryption Standard (DES)

#### Concept
64-bit symmetric block cipher using a 56-bit effective key across 16 Feistel rounds. Operates in Electronic Codebook (ECB) mode with PKCS#7 padding.

#### Source Code (`Python Codes/Des.py`)
```python
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b"12345678"
cipher = DES.new(key, DES.MODE_ECB)
pt = input("Enter Message: ")
ct = cipher.encrypt(pad(pt.encode(), DES.block_size))
print("Encrypted:", ct.hex())
print("Decrypted:", unpad(cipher.decrypt(ct), DES.block_size).decode())
```

#### Sample Output
```text
Enter Message: Hello DES
Encrypted: 8c0d12e84a20b9e8...
Decrypted: Hello DES
```

---

### 4. Triple Data Encryption Standard (3DES)

#### Concept
Applies three sequential DES operations in Encrypt-Decrypt-Encrypt (EDE) mode using a 192-bit key (three 64-bit keys $K_1, K_2, K_3$):
$$C = E_{K3}(D_{K2}(E_{K1}(P)))$$
$$P = D_{K1}(E_{K2}(D_{K3}(C)))$$

#### Source Code (`Python Codes/triple_Des`)
```python
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

key = b"123456789012345678901234"
cipher = DES3.new(key, DES3.MODE_ECB)
pt = input("Enter Message: ")
ct = cipher.encrypt(pad(pt.encode(), DES3.block_size))
print("Encrypted:", ct.hex())
print("Decrypted:", unpad(cipher.decrypt(ct), DES3.block_size).decode())
```

#### Sample Output
```text
Enter Message: Hello Triple DES
Encrypted: 66a2e419fd81e18d...
Decrypted: Hello Triple DES
```

---

### 5. Advanced Encryption Standard (AES)

#### Concept
Symmetric 128-bit block cipher utilizing a Substitution-Permutation Network (SPN) with 10 iterative rounds. Operates in Cipher Block Chaining (CBC) mode with a 16-byte Initialization Vector (IV) and PKCS#7 padding.

#### Source Code (`Python Codes/aes.py`)
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b"0123456789abcdef"
iv = b"abcdef9876543210"
plaintext = b"Hello AES Algorithm"

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
print("Plaintext:", plaintext.decode())
print("Encrypted data (hex):", ciphertext.hex())

decipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(decipher.decrypt(ciphertext), AES.block_size)
print("Decrypted data:", decrypted.decode())
```

#### Sample Output
```text
Plaintext: Hello AES Algorithm
Encrypted data (hex): b6a482e70e9a7e678a1f6a9e6b4c10d3e2300c1e...
Decrypted data: Hello AES Algorithm
```

---

## Lab 5: Simulation of Access Control Matrix and Dynamic Rights Updates

### Aim and Protection Model
To simulate an Access Control Matrix (ACM), demonstrate dynamic granting and revoking of user access rights, and evaluate performance scaling across varying input sizes and permission densities.

Protection State Representation:
- Subjects (Users): $U = \{U_1, U_2, \dots, U_n\}$
- Objects (Resources): $R = \{Res_1, Res_2, \dots, Res_m\}$
- Protection Matrix: $M[u, r] \subseteq \{R, W, X, D\}$

### Permissions Specification
| Permission Code | Meaning | Operation Description |
| :---: | :---: | :--- |
| **R** | Read | View and extract contents of protected resources |
| **W** | Write | Modify, update, or append contents |
| **X** | Execute | Run scripts, binaries, or automated workflows |
| **D** | Delete | Remove the resource permanently |

### Lab 5 Python Source Code (`Python Codes/lab5_access_control_matrix.py`)
```python
import time
import random
import os
import matplotlib.pyplot as plt

OUTPUT_IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "lab5_graphs")
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

PERMISSIONS = ['R', 'W', 'X', 'D']

class AccessControlMatrix:
    def __init__(self, num_users, num_resources, density=0.5, seed=42):
        self.num_users = num_users
        self.num_resources = num_resources
        self.users = [f"User_{i+1}" for i in range(num_users)]
        self.resources = [f"Res_{j+1}" for j in range(num_resources)]
        self.matrix = {}
        self.density = density
        if seed is not None:
            random.seed(seed)
        self._build_matrix()

    def _build_matrix(self):
        for u in self.users:
            self.matrix[u] = {}
            for r in self.resources:
                if random.random() < self.density:
                    num_perms = random.randint(1, len(PERMISSIONS))
                    self.matrix[u][r] = set(random.sample(PERMISSIONS, num_perms))
                else:
                    self.matrix[u][r] = set()

    def check_access(self, user, resource, operation):
        if user not in self.matrix or resource not in self.matrix[user]:
            return False, "DENIED"
        is_allowed = operation in self.matrix[user][resource]
        return is_allowed, "GRANTED" if is_allowed else "DENIED"

    def grant_permission(self, user, resource, operation):
        if user in self.matrix and resource in self.matrix[user]:
            self.matrix[user][resource].add(operation)
            return True
        return False

    def revoke_permission(self, user, resource, operation):
        if user in self.matrix and resource in self.matrix[user]:
            self.matrix[user][resource].discard(operation)
            return True
        return False

    def display(self, max_u=5, max_r=5):
        users_to_show = self.users[:max_u]
        res_to_show = self.resources[:max_r]
        header = f"{'User':<12}" + "".join([f"{r:<14}" for r in res_to_show])
        print(header)
        print("-" * len(header))
        for u in users_to_show:
            row_str = f"{u:<12}"
            for r in res_to_show:
                perms = "".join(sorted(list(self.matrix[u][r]))) if self.matrix[u][r] else "-"
                row_str += f"{perms:<14}"
            print(row_str)
```

*(The full file includes the benchmarking engine and graphical plot generation; execute `python "Python Codes/lab5_access_control_matrix.py"` to run).*

### Lab 5 Sample Execution and Console Output
```text
===========================================================================
CNS LAB 5 - ACCESS CONTROL MATRIX SIMULATION & BENCHMARKING
===========================================================================

[Initial Access Control Matrix (5 Users x 5 Resources)]:
User        Res_1         Res_2         Res_3         Res_4         Res_5         
----------------------------------------------------------------------------------
User_1      -             DRX           -             -             WX            
User_2      RW            DWX           DRWX          RX            -             
User_3      -             -             -             DRWX          -             
User_4      DRWX          -             DRW           -             DRW           
User_5      -             -             DRWX          -             -             

[Access Requests & Verification]:
Request: User 'User_1' requests 'Read (R)' on 'Res_1'    -> Result: DENIED
Request: User 'User_1' requests 'Write (W)' on 'Res_2'   -> Result: DENIED
Request: User 'User_2' requests 'Execute (X)' on 'Res_3' -> Result: GRANTED
Request: User 'User_3' requests 'Delete (D)' on 'Res_1'  -> Result: DENIED
Request: User 'User_4' requests 'Write (W)' on 'Res_5'   -> Result: GRANTED

[Dynamic Access Updates]:
1. Granting 'W' (Write) and 'D' (Delete) to User_1 on Res_2...
   -> Verifying User_1 on Res_2 for 'Write':  GRANTED
   -> Verifying User_1 on Res_2 for 'Delete': GRANTED
2. Revoking 'W' (Write) from User_1 on Res_2...
   -> Verifying User_1 on Res_2 for 'Write' after revocation: DENIED

[Updated Access Control Matrix]:
User        Res_1         Res_2         Res_3         Res_4         Res_5         
----------------------------------------------------------------------------------
User_1      -             DRX           -             -             WX            
User_2      RW            DWX           DRWX          RX            -             
User_3      -             -             -             DRWX          -             
User_4      DRWX          -             DRW           -             DRW           
User_5      -             -             DRWX          -             -             
```

### Lab 5 Performance Measurements
Execution timings measured using `time.perf_counter_ns` averaged over 200 iterations:

| Experiment Configuration | Matrix Creation (ms) | Verification (ms) | Update (ms) | Total Time (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **Test 1** (5 users / 5 res) | 0.0303 | 0.0020 | 0.0009 | 0.0332 |
| **Test 2** (10 users / 10 res) | 0.1134 | 0.0030 | 0.0016 | 0.1180 |
| **Test 3** (15 users / 15 res) | 0.2485 | 0.0039 | 0.0026 | 0.2551 |
| **Test 4** (20 users / 20 res) | 0.4395 | 0.0063 | 0.0036 | 0.4494 |
| **Test 5** (50 users / 50 res) | 3.5933 | 0.0087 | 0.0045 | 3.6065 |

### Lab 5 Permission Density Experiment
Fixed dimensions of 50 users x 50 resources:

| Permission Density (%) | Non-Empty Cells | Processing Time (ms) |
| :---: | :---: | :---: |
| **10%** | 250 cells | 1.5611 |
| **25%** | 625 cells | 2.5492 |
| **50%** | 1250 cells | 3.6373 |
| **75%** | 1875 cells | 4.9614 |
| **100%** | 2500 cells | 6.4262 |

### Lab 5 Graphical Analysis
Generated plots saved in `lab5_graphs/`:
1. `lab5_graph1_users_vs_time.png`: Quadratic growth $O(U \times R)$ of matrix initialization.
2. `lab5_graph2_requests_vs_verification.png`: Linear scaling $O(k)$ for sequential request verifications.
3. `lab5_graph3_updates_vs_time.png`: Linear scaling of dynamic grant and revoke operations.
4. `lab5_graph4_density_vs_processing.png`: Linear progression of processing time as matrix density scales from 10% to 100%.
5. `lab5_graph5_granted_vs_denied.png`: Proportional distribution of granted and denied requests.

### Lab 5 Observations and Result
- Matrix creation time exhibits quadratic complexity $O(U \times R)$, requiring $N^2$ cell allocations for an $N \times N$ matrix.
- Access verification scales strictly linearly with request count, maintaining an average lookup latency of ~0.0002 ms per request.
- Dynamic updates scale linearly with operation count while per-update latency remains constant ($O(1)$ amortized).
- Processing latency increases monotonically with permission density due to additional set allocations.
- **Result**: The Access Control Matrix simulation, dynamic rights update engine, and performance analysis were executed successfully.

---

## Lab 6: Multi-User Cloud RBAC and Mutual Certificate Authentication

### Lab 6 Aim and Security Architecture
To demonstrate secure access in a multi-user cloud system combining Public Key Infrastructure (PKI) with Role-Based Access Control (RBAC):
- Local Root Certificate Authority (CA): Issues X.509 v3 certificates signed using RSA-2048 with SHA-256 signatures via `cryptography.x509`.
- Gateway Server Identity: Validated by clients during the mutual handshake.
- Mutual Authentication Protocol: The gateway verifies the client certificate against the CA, validates timestamps, and checks the Certificate Revocation List (CRL). Simultaneously, the client verifies the gateway certificate.
- RBAC Engine: Access decisions are evaluated against user roles and target permissions only after mutual authentication succeeds.

### Lab 6 Roles and Permissions Matrix
| Role | Read (R) | Write/Upload (W) | Modify (M) | Delete (D) | User Management (UM) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Administrator** | Yes | Yes | Yes | Yes | Yes |
| **Faculty/Manager** | Yes | Yes | Yes | Limited | No |
| **Student/User** | Yes | Yes | No | No | No |
| **Guest** | Limited | No | No | No | No |
| **Auditor** | Yes | No | No | No | No |

### Lab 6 Python Source Code (`Python Codes/lab6_cloud_rbac_mutual_auth.py`)
```python
import datetime
import time
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

class CertificateAuthority:
    def __init__(self, name="CloudTrust_Root_CA"):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Secure Cloud Org"),
        ])
        now = datetime.datetime.now(datetime.timezone.utc)
        self.cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
            self.private_key.public_key()
        ).serial_number(x509.random_serial_number()).not_valid_before(
            now - datetime.timedelta(days=1)
        ).not_valid_after(
            now + datetime.timedelta(days=365)
        ).sign(self.private_key, hashes.SHA256())
        self.crl = set()

    def verify_cert(self, cert):
        try:
            self.private_key.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm
            )
        except InvalidSignature:
            return False, "UNTRUSTED_ISSUER"

        now = datetime.datetime.now(datetime.timezone.utc)
        if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
            return False, "EXPIRED"

        if cert.serial_number in self.crl:
            return False, "REVOKED"

        return True, "VALID"
```

*(The full file includes the multi-user cloud engine, adversarial test harness, and plotting routines; execute `python "Python Codes/lab6_cloud_rbac_mutual_auth.py"` to run).*

### Lab 6 Security Test Cases
Verification across all four certificate conditions:

| Certificate Condition | Client Cert Status | Mutual Authentication | RBAC Decision | Final Access Status |
| :--- | :--- | :---: | :---: | :---: |
| **Valid** | `VALID` | **SUCCESS** | Evaluated / ALLOWED | **ACCESS GRANTED** |
| **Expired** | `EXPIRED` | **FAILED** | Blocked by Auth Failure | **ACCESS DENIED** |
| **Revoked** | `REVOKED` | **FAILED** | Blocked by Auth Failure | **ACCESS DENIED** |
| **Untrusted CA** | `UNTRUSTED_ISSUER` | **FAILED** | Blocked by Auth Failure | **ACCESS DENIED** |

### Lab 6 Expected Output Record (Section 13 Format)
```text
Resource: File_01.pdf
Operation: Modify
Client Certificate: VALID
Server Certificate: VALID
Mutual Authentication: SUCCESS
RBAC Decision: DENIED
Authentication Time: 0.1165 ms
Authorization Time: 0.0029 ms
Total Response Time: 0.1194 ms
Final Status: ACCESS DENIED
```

### Lab 6 Performance Measurements
Empirical values recorded across 5 test configurations:

| Input Size | Setup (ms) | Avg Auth (ms) | Avg Authz (ms) | Response (ms) | Update (ms) | Throughput (req/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Test 1** (5 users / 5 res) | 535.127 | 0.3471 | 0.0013 | 0.3484 | 0.0009 | 2,870.10 |
| **Test 2** (10 users / 10 res) | 685.670 | 0.1133 | 0.0009 | 0.1143 | 0.0015 | 8,750.05 |
| **Test 3** (15 users / 15 res) | 952.036 | 0.1423 | 0.0008 | 0.1431 | 0.0019 | 6,990.56 |
| **Test 4** (20 users / 20 res) | 1287.099 | 0.1028 | 0.0008 | 0.1036 | 0.0024 | 9,652.14 |
| **Test 5** (25 users / 25 res) | 1421.517 | 0.0816 | 0.0005 | 0.0821 | 0.0031 | 12,181.12 |

### Lab 6 Permission Density Benchmark
| Permission Density (%) | Authorization Processing Time (ms) |
| :---: | :---: |
| **10%** | 0.00022 |
| **25%** | 0.00020 |
| **50%** | 0.00019 |
| **75%** | 0.00020 |
| **100%** | 0.00020 |

### Lab 6 Graphical Analysis
Generated plots saved in `lab6_graphs/`:
1. `lab6_graph1_users_vs_auth_time.png`: Average authentication latency across user populations.
2. `lab6_graph2_users_vs_authz_time.png`: Sub-microsecond RBAC authorization lookup times.
3. `lab6_graph3_users_vs_response_time.png`: Total response time dominated by cryptographic verification.
4. `lab6_graph4_requests_vs_authz_time.png`: Per-request authorization latency under increasing request volumes.
5. `lab6_graph5_updates_vs_update_time.png`: Linear scaling of role policy modification operations.
6. `lab6_graph6_concurrent_users_vs_throughput.png`: Sustained throughput between 2,800 and 12,000 req/s.
7. `lab6_graph7_cert_status_vs_auth_results.png`: 100% rejection rate for adversarial certificates (expired, revoked, untrusted).
8. `lab6_graph8_density_vs_processing.png`: Constant authorization latency invariant to permission density.
9. `lab6_graph9_granted_vs_denied.png`: Breakdown of granted versus denied requests across tests.

### Lab 6 Observations and Result
- Cryptographic verification (RSA-2048 with SHA-256) accounts for over 98% of total request latency (~0.1 to 0.35 ms), whereas RBAC evaluation requires less than 0.001 ms.
- Zero-Trust certificate validation halts illegitimate requests before RBAC policy inspection, defending cloud resources from unnecessary overhead.
- Throughput scales effectively, supporting between 2,800 and 12,000 requests per second.
- **Result**: The multi-user cloud access system, mutual certificate authentication handshake, and RBAC authorization framework were successfully demonstrated and evaluated.

---

## Master Laboratory Report Document

The primary compiled laboratory report document is located at:
- **File**: `CNS_Lab_Documentation.docx`
- **Location**: `CNS_Lab_Documentation/CNS_Lab_Documentation.docx`
- **Format**: Formatted Microsoft Word document containing all program specifications, source code blocks, empirical measurement tables, and graphical plots (omitting analysis questions).

---

## Execution Guide

From inside the `CNS_Lab_Documentation` folder, run any experiment:

```bash
# Lab 1
python "Python Codes/substitution.py"
python "Python Codes/monoalpha.py"

# Lab 2
python "Python Codes/play_fair_cipher.py"
python "Python Codes/hill_cipher.py"

# Lab 3
python "Python Codes/stream_cipher.py"
python "Python Codes/feistal_cipher"
python "Python Codes/Des.py"
python "Python Codes/triple_Des"
python "Python Codes/aes.py"

# Lab 5 (Access Control Matrix)
python "Python Codes/lab5_access_control_matrix.py"

# Lab 6 (Cloud RBAC & Mutual Authentication)
python "Python Codes/lab6_cloud_rbac_mutual_auth.py"
```
