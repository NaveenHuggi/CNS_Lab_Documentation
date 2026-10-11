# Cryptography and Network Security (CNS) Laboratory

## Overview

This repository provides complete implementations, benchmark evaluations, and formal laboratory documentation for experiments in Cryptography and Network Security (CNS). The laboratory curriculum covers classical substitution and polygraphic ciphers, modern symmetric block and stream ciphers, access control protection mechanisms, and cloud security architectures integrating Public Key Infrastructure (PKI) with Role-Based Access Control (RBAC).

All source programs are implemented in Python with support for high-precision performance telemetry, automated test harnesses, and publication-ready graphical plots.

---

## Environment and Dependencies

### Prerequisites
- Operating System: Windows, Linux, or macOS
- Python Version: Python 3.10, 3.11, or 3.12 (64-bit recommended)

### Required Libraries
The laboratory implementations utilize standard Python libraries along with cryptographic and numerical packages:
- `pycryptodome` (>= 3.20.0): Implements DES, 3DES, AES, and ARC4 primitives.
- `cryptography` (>= 42.0.0): Implements X.509 certificate generation, RSA key pairs, and digital signature validation.
- `matplotlib` (>= 3.8.0): Generates graphical benchmark plots.
- `python-docx` (>= 1.1.0): Compiles structured Microsoft Word laboratory reports.

### Installation
Install the necessary packages using pip:

```bash
pip install pycryptodome cryptography matplotlib python-docx
```

---
## Detailed Experiment Specifications

### Lab 1: Classical Substitution and Monoalphabetic Ciphers

#### 1. Additive Substitution Cipher (`substitution.py`)
- Theoretical Model: Monoalphabetic shift cipher where each character in the plaintext is shifted by a fixed integer key $k$ modulo 26:
  $$C_i = (P_i + k) \pmod{26}$$
  $$P_i = (C_i - k) \pmod{26}$$
- Implementation Details:
  - Alphabet: 26 lowercase English characters (`a` through `z`).
  - Key: Fixed shift $k = 3$.
  - Execution command:
    ```bash
    python substitution.py
    ```
- Sample Output:
  ```text
  ['k', 'h', 'o', 'o', 'r']
  ['h', 'e', 'l', 'l', 'o']
  ```

#### 2. General Monoalphabetic Cipher (`monoalpha.py`)
- Theoretical Model: Uses an arbitrary permutation of the 26-letter alphabet to construct a one-to-one mapping between plaintext characters and ciphertext characters.
- Implementation Details:
  - Includes validation functions `validate_alphabets()` checking for mismatched length and duplicate symbols.
  - Case preservation and handling of non-alphabetic characters (digits and punctuation remain intact).
  - Configurable plaintext and ciphertext mapping tables with bidirectional dictionary lookup.
- Sample Output:
  ```text
  Plaintext: Hello Bhai 123!
  Encrypted: Khoor Ekdl 123!
  Decrypted: Hello Bhai 123!
  ```

---

### Lab 2: Polyalphabetic and Polygraphic Ciphers

#### 1. Playfair Cipher (`play_fair_cipher.py`)
- Theoretical Model: Polygraphic substitution cipher encrypting pairs of letters (digraphs) using a 5x5 key matrix generated from a keyword.
- Rules:
  - Character normalisation: Letters `I` and `J` share the same matrix position.
  - Digraph preparation: If both characters in a pair are identical, a filler character (`z`) is inserted. If the length is odd, a trailing filler (`z`) is appended.
  - Same row rule: Replace each character with the letter immediately to its right (modulo 5).
  - Same column rule: Replace each character with the letter immediately below it (modulo 5).
  - Rectangle rule: Each character is replaced by the letter in its own row and the column of the other character.
  - Decryption reverses the column and row shift directions (shift left / shift up).
- Sample Input and Output:
  ```text
  Key: Monarchy
  Plaintext: instruments

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

#### 2. Hill Cipher (`hill_cipher.py`)
- Theoretical Model: Polygraphic block cipher based on modular linear algebra over $\mathbb{Z}_{26}$. Plaintext blocks of size $m=2$ are represented as vectors $\mathbf{P} = \begin{bmatrix} p_1 & p_2 \end{bmatrix}^T$ and encrypted using key matrix $\mathbf{K}$:
  $$\mathbf{C} = \mathbf{K} \cdot \mathbf{P} \pmod{26}$$
  $$\mathbf{P} = \mathbf{K}^{-1} \cdot \mathbf{C} \pmod{26}$$
- Modular Matrix Inversion ($2 \times 2$):
  $$\det(\mathbf{K}) = (ad - bc) \pmod{26}$$
  $$\mathbf{K}^{-1} = \det(\mathbf{K})^{-1} \cdot \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \pmod{26}$$
  Where $\det(\mathbf{K})^{-1}$ is the modular multiplicative inverse such that $(\det(\mathbf{K}) \cdot \det(\mathbf{K})^{-1}) \equiv 1 \pmod{26}$.
- Sample Input and Output:
  ```text
  Key Matrix:
  [3, 3]
  [2, 5]

  Determinant: 9 mod 26
  Modular Inverse of Determinant: 3 (since 9 * 3 = 27 = 1 mod 26)

  Inverse Key Matrix:
  [15, 17]
  [20, 9]

  Plaintext: help
  Ciphertext: hiat
  Decrypted Text: help
  ```

---

### Lab 3: Modern Symmetric Block and Stream Ciphers

#### 1. ARC4 Stream Cipher (`stream_cipher.py`)
- Theoretical Model: Symmetric stream cipher using the Alleged RC4 (ARC4) algorithm. Produces a pseudo-random keystream byte-by-byte via Key-Scheduling Algorithm (KSA) and Pseudo-Random Generation Algorithm (PRGA), combined with plaintext bytes using bitwise XOR.
- Sample Output:
  ```text
  Enter Plain Text: Hello
  Encrypted: 492e448b3b
  Decrypted: Hello
  ```

#### 2. Feistel Cipher Network (`feistal_cipher`)
- Theoretical Model: Demonstrates an iterative symmetric Feistel network structure over 4 rounds. Each round divides the block into two equal halves $(L_i, R_i)$:
  $$L_{i+1} = R_i$$
  $$R_{i+1} = L_i \oplus F(R_i, K)$$
- Sample Output:
  ```text
  Before: 10 20
  After: 20 17
  ```

#### 3. Data Encryption Standard (`Des.py`)
- Theoretical Model: 64-bit symmetric block cipher using a 56-bit effective key with 16 rounds of Feistel permutations.
- Mode of Operation: Electronic Codebook (ECB) with PKCS#7 padding via `Crypto.Cipher.DES`.
- Sample Output:
  ```text
  Enter Message: Hello DES
  Encrypted: 8c0d12e84a20b9e8...
  Decrypted: Hello DES
  ```

#### 4. Triple DES (`triple_Des`)
- Theoretical Model: Applies three successive DES stages in Encrypt-Decrypt-Encrypt (EDE) sequence using a 192-bit key (three independent 64-bit keys $K_1, K_2, K_3$):
  $$C = E_{K3}(D_{K2}(E_{K1}(P)))$$
  $$P = D_{K1}(E_{K2}(D_{K3}(C)))$$
- Provides 112 bits of effective security against meet-in-the-middle attacks.

#### 5. Advanced Encryption Standard (`aes.py`)
- Theoretical Model: Substitution-Permutation Network (SPN) block cipher operating on 128-bit state matrices over Galois Field $GF(2^8)$.
- Mode of Operation: Cipher Block Chaining (CBC) with a 128-bit Initialization Vector (IV) and PKCS#7 padding via `Crypto.Cipher.AES`.
- Sample Output:
  ```text
  Plaintext: Hello AES Algorithm
  Encrypted data (hex): b6a482e70e9a7e678a1f6a9e6b4c10d3e2300c1e...
  Decrypted data: Hello AES Algorithm
  ```

---

### Lab 5: Simulation of Access Control Matrix (ACM) and Dynamic Rights Updates

#### 1. Objective and Architecture (`lab5_access_control_matrix.py`)
Simulates an Access Control Matrix (ACM) representing system protection state:
- Subjects (Users): $U = \{U_1, U_2, \dots, U_n\}$
- Objects (Resources): $R = \{Res_1, Res_2, \dots, Res_m\}$
- Access Rights: $M[u, r] \subseteq \{R, W, X, D\}$
  - $R$: Read
  - $W$: Write
  - $X$: Execute
  - $D$: Delete
- Automated Generation: Configurable matrix dimension and permission density factor.
- Dynamic Operations: Dynamic granting of new rights, revoking of existing rights, and state verification before and after updates.

#### 2. Experimental Benchmark Results
Measured across 5 benchmark configurations with repeated measurement loops:

| Input Configuration | Matrix Creation Time (ms) | Verification Time (ms) | Update Time (ms) | Total Time (ms) |
| :--- | :---: | :---: | :---: | :---: |
| Test 1 (5 users / 5 resources) | 0.0303 | 0.0020 | 0.0009 | 0.0332 |
| Test 2 (10 users / 10 resources) | 0.1134 | 0.0030 | 0.0016 | 0.1180 |
| Test 3 (15 users / 15 resources) | 0.2485 | 0.0039 | 0.0026 | 0.2551 |
| Test 4 (20 users / 20 resources) | 0.4395 | 0.0063 | 0.0036 | 0.4494 |
| Test 5 (50 users / 50 resources) | 3.5933 | 0.0087 | 0.0045 | 3.6065 |

#### 3. Permission Density Experiment (50 Users x 50 Resources)

| Permission Density | Populated Cells | Processing Time (ms) |
| :---: | :---: | :---: |
| 10% | 250 cells | 1.5611 |
| 25% | 625 cells | 2.5492 |
| 50% | 1250 cells | 3.6373 |
| 75% | 1875 cells | 4.9614 |
| 100% | 2500 cells | 6.4262 |

#### 4. Generated Plots
All figures are saved to `d:/CNS_LAB/lab5_graphs/`:
- `lab5_graph1_users_vs_time.png`: Number of Users vs Execution Time.
- `lab5_graph2_requests_vs_verification.png`: Number of Access Requests vs Verification Time.
- `lab5_graph3_updates_vs_time.png`: Number of Access Updates vs Update Time.
- `lab5_graph4_density_vs_processing.png`: Permission Density vs Processing Time.
- `lab5_graph5_granted_vs_denied.png`: Ratio of Granted vs Denied Requests Across Runs.

#### 5. Technical Observations
- Matrix Creation Time exhibits quadratic algorithmic complexity $O(U \times R)$, requiring $N^2$ cell allocations for an $N \times N$ matrix.
- Access Verification Time scales linearly $O(k)$ with request count, maintaining an average lookup latency of ~0.0002 ms per request via hash table indexing.
- Dynamic Update Time scales linearly with update volume, verifying that dictionary and set operations execute in deterministic $O(1)$ amortized time.
- Processing latency increases monotonically with permission density due to increased set instantiations.

---

### Lab 6: Multi-User Cloud RBAC and Mutual Certificate Authentication

#### 1. Objective and Architecture (`lab6_cloud_rbac_mutual_auth.py`)
Implements an end-to-end cloud protection architecture combining Public Key Infrastructure (PKI) with Role-Based Access Control (RBAC):
- Local Certificate Authority (CA): Issues X.509 v3 certificates signed with RSA-2048 and SHA-256 signatures using `cryptography.x509`.
- Server Gateway Certificate: Certified server identity for client-side trust verification.
- Client User Certificates: Generated with distinct Common Names (CN), valid timestamp ranges, and serial numbers.
- Mutual Authentication Protocol:
  - Step 1: Gateway validates client certificate signature against CA public key, checks validity timestamps, and queries the Certificate Revocation List (CRL).
  - Step 2: Client validates server certificate signature against root CA public key.
  - Mutual authentication succeeds only when both peer certificates pass all security checks.
- RBAC Authorization Engine: Once authenticated, requests are evaluated against central role permission matrices:
  - Administrator: Read, Write/Upload, Modify, Delete, User Management.
  - Faculty/Manager: Read, Write/Upload, Modify, Limited Delete.
  - Student/User: Read, Write/Upload.
  - Guest: Limited Read.
  - Auditor: Read.

#### 2. Experimental Benchmark Results

| Input Size | Setup Time (ms) | Avg Auth (ms) | Avg Authz (ms) | Response Time (ms) | Update Time (ms) | Throughput (req/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Test 1 (5 users / 5 res) | 535.127 | 0.3471 | 0.0013 | 0.3484 | 0.0009 | 2,870.10 |
| Test 2 (10 users / 10 res) | 685.670 | 0.1133 | 0.0009 | 0.1143 | 0.0015 | 8,750.05 |
| Test 3 (15 users / 15 res) | 952.036 | 0.1423 | 0.0008 | 0.1431 | 0.0019 | 6,990.56 |
| Test 4 (20 users / 20 res) | 1287.099 | 0.1028 | 0.0008 | 0.1036 | 0.0024 | 9,652.14 |
| Test 5 (25 users / 25 res) | 1421.517 | 0.0816 | 0.0005 | 0.0821 | 0.0031 | 12,181.12 |

#### 3. Security Boundary Verification

| Certificate Condition | Client Cert Status | Mutual Authentication | RBAC Decision | Final Access Status |
| :--- | :--- | :---: | :---: | :---: |
| Valid | VALID | SUCCESS | Evaluated / ALLOWED | ACCESS GRANTED |
| Expired | EXPIRED | FAILED | Blocked by Auth Failure | ACCESS DENIED |
| Revoked | REVOKED | FAILED | Blocked by Auth Failure | ACCESS DENIED |
| Untrusted CA | UNTRUSTED_ISSUER | FAILED | Blocked by Auth Failure | ACCESS DENIED |

#### 4. Section 13 Decision Output Format
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

#### 5. Generated Plots
All figures are saved to `d:/CNS_LAB/lab6_graphs/`:
- `lab6_graph1_users_vs_auth_time.png`: Number of Users vs Authentication Time.
- `lab6_graph2_users_vs_authz_time.png`: Number of Users vs Authorization Time.
- `lab6_graph3_users_vs_response_time.png`: Number of Users vs Total Access Response Time.
- `lab6_graph4_requests_vs_authz_time.png`: Number of Access Requests vs Authorization Time.
- `lab6_graph5_updates_vs_update_time.png`: Number of Access Updates vs Update Time.
- `lab6_graph6_concurrent_users_vs_throughput.png`: Concurrent Users vs Throughput.
- `lab6_graph7_cert_status_vs_auth_results.png`: Certificate Status vs Authentication Success/Rejection.
- `lab6_graph8_density_vs_processing.png`: Permission Density vs Authorization Processing Time.
- `lab6_graph9_granted_vs_denied.png`: Granted Requests vs Denied Requests Across Runs.

#### 6. Technical Observations
- Asymmetric cryptographic signature validation (RSA-2048 with SHA-256) accounts for greater than 98% of total request latency (~0.1 to 0.35 ms per mutual handshake), while RBAC authorization lookup executes in less than 0.001 ms.
- Zero-Trust enforcement prevents unauthorized or corrupted certificates from accessing authorization logic, isolating the internal policy engine.
- System throughput scales effectively, maintaining rates between 2,800 and 12,000 requests per second.
- Permission density has no impact on authorization latency due to constant-time set lookups.

---

## Laboratory Documentation Report

### Report Summary
- Document Name: `CNS_Lab5_Lab6_Implementation_Report.docx`
- File Size: Approximately 1.86 MB
- Generator Script: `generate_report.py`

### Document Contents
1. Formal header, course title, and institutional banner.
2. Complete mathematical formulations, architecture diagrams, and permission models.
3. Formatted source code listings with monospaced typography.
4. Comprehensive empirical data tables containing actual benchmark figures.
5. High-resolution callout boxes showing detailed console outputs and Section 13 decision records.
6. All 14 embedded graphical plots with descriptive technical captions.
7. Technical observations and final experimental conclusions.
8. Analysis questions are omitted in accordance with specification instructions.

### Compiling the Report
To recompile the Word document:

```bash
python generate_report.py
```

---

## Execution Instructions

Run any experiment directly from the workspace root:

```bash
# Run Lab 1
python substitution.py
python monoalpha.py

# Run Lab 2
python play_fair_cipher.py
python hill_cipher.py

# Run Lab 3
python stream_cipher.py
python feistal_cipher
python Des.py
python triple_Des
python aes.py

# Run Lab 5 (Access Control Matrix)
python lab5_access_control_matrix.py

# Run Lab 6 (Cloud RBAC & Mutual Auth)
python lab6_cloud_rbac_mutual_auth.py

# Compile Comprehensive DOCX Report
python generate_report.py
```
