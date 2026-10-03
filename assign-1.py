"""
FINA 4340 - Assignment 1: Basics of Cryptography
"""

import hashlib
import json

print("PROBLEM 0: Number Representation")

# Problem 0 a
for n in (11, 12):
    print(f"{n} in binary  = {bin(n)[2:]}")

# Problem 0 b
for n in (21, 22):
    print(f"{n} in binary  = {bin(n)[2:]}")
print("Pattern: 21 = 10101 and 22 = 10110, only the last two bits change because only the 'ones' place changed")

# Problem 0 c
for n in (21, 22):
    print(f"{n} in hex     = {hex(n)[2:]}")
print("Pattern: 21 = 0x15 and 22 = 0x16 -- hex digits increase by 1 one-for-one")

# Problem 0 d
print("Comparing hexadecimal numbers (converted to decimal to check):")
pairs = [("a10", "a21"), ("56f", "661"), ("9d5", "9b9"), ("10a9", "10a8"), ("dd5", "da9")]
for a, b in pairs:
    va, vb = int(a, 16), int(b, 16)
    bigger = a if va > vb else b
    print(f"  {a} (={va}) vs {b} (={vb})  ->  {bigger} is greater")


print("PROBLEM 1: Asymmetric Encryption")
# 1.a finding private and public keys
p, q = 7, 11
n = p * q                 # public modulus
phi = (p - 1) * (q - 1)   # (private) used to derive d
e = 11                    # public exponent
d = pow(e, -1, phi)       # private exponent
print(f"Private keys:  p = {p}, q = {q}, d = {d}")
print(f"Public keys:   n = p*q = {n}, e = {e}")

# 1.b: Encrypt the message "W"
msg = ord("W")
print(f'\nASCII of "W" = {msg}')
encrypted_w = pow(msg, e, n)
print(f"Encrypted message (W^e mod n): {encrypted_w}")
print("since the message (87) is larger than n (77), this violates RSA's")
print("requirement that the message be smaller than n, so decrypting this specific")
print("ciphertext will not correctly recover 'W'. shown below:")
print("  decrypt(encrypt(87)) =", pow(encrypted_w, d, n), "(m != m')")

# 1.c: Decrypt "129" 
c1 = 129    
dec1 = pow(c1, d, n)
print(f'\nDecrypt "129": 129^d mod n = {dec1}  ->  chr({dec1}) = {chr(dec1)!r} ')

# 1.4: Decrypt "231"
c2 = 231
dec2 = pow(c2, d, n)
print(f'Decrypt "231": 231^d mod n = {dec2}  ->  chr({dec2}) = {chr(dec2)!r} ')


# --- 1.5: Does a set of private keys always lead to the same public keys? ---
print("""Does a set of private keys always lead to the same set of public keys?
No. The public key pair (n, e) depends on the private primes p and q through
n = p*q, but the exponent e is not unique. Any e that is coprime with
phi(n) = (p-1)(q-1) is valid.
""")

# --- 1.6: Pick a second set of keys, encrypt "!" by hand, verify in Python ---
p2, q2 = 5, 11
n2 = p2 * q2                    # n = 55
phi2 = (p2 - 1) * (q2 - 1)      # phi = 40
e2 = 3                          # gcd(3, 40) = 1
d2 = pow(e2, -1, phi2)          # d = 27
msg2 = ord("!")                 # ASCII of "!" = 33

print(f"Second key set: p = {p2}, q = {q2}  ->  n = {n2}, phi(n) = {phi2}, e = {e2}, d = {d2}")
print(f'ASCII of "!" = {msg2}')
print("""33^3 mod 55:
  33^2 = 1089  ->  1089 mod 55 = 44
  33^3 = 33 * 44 = 1452  ->  1452 mod 55 = 22
  So by hand: encrypted "!" = 22
""")
encrypted= pow(msg2, e2, n2)
print("Python verification: pow(33, 3, 55) =", encrypted)
decrypted = pow(encrypted, d2, n2)
print("Decrypting back:", decrypted, "->", chr(decrypted))

print("PROBLEM 2: Hash Functions / SHA-256")

# 2.a: Three properties of a "good" hash function
print("""
Three properties of a "good" cryptographic hash function:
1. if we know the output message AND a portion of the input message, it must still be unfeasible to find the rest of the input message.
2. given the output of a hash function, it must be unfeasible to find or infer the input message that produced it.
3. it must be computationally impossible to find 2 distinct messages m1 and m2 that hash to the same value.
""")

# 2.b 
messages = ["Hello", "Mom", "Dad", "I don't like Python"]
print("Digests:")
for m in messages:
    print(f'  SHA256("{m}") = {hashlib.sha256(m.encode()).hexdigest()}')

# 2.c
target_digest = "e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683"
print("\nLottery (outcomes 0-10), target digest:", target_digest)
winner = None
for i in range(0, 11):
    if hashlib.sha256(str(i).encode()).hexdigest() == target_digest:
        winner = i
        break
print(f"Winning number found by brute force: {winner}")
print("""Is SHA-256 a "good" hashing function? Yes. We could only find the answer
because there were only 11 possibilities, allowing us to hash every
possible outcome and compare. This is different from reversing the hash
mathematically.""")

#2.d
print("""
SHA-1 was officially deprecated by NIST (2011) after cryptanalytic weaknesses
were found; in 2017, Google and CWI Amsterdam produced an actual SHA-1 collision
("SHAttered"), confirming it is broken and should not be used.
Yes, there is a SHA-3 family. It was standardized by NIST in 2015 and is built on
a completely different design rather than the
Merkle-Damgard structure used by SHA-1/SHA-2.
Ethereum uses a hash function from the SHA-3 family, specifically
Keccak-256, a close variant of SHA3-256, for its addresses and transaction
hashing.
""")

# --- 2.5: Find a message with digest starting with "a" ---
i = 0
while True:
    msg = str(i)
    digest = hashlib.sha256(msg.encode()).hexdigest()
    if digest.startswith("a"):
        print(f'Message "{msg}" -> digest {digest}  (starts with "a")')
        break
    i += 1

# --- 2.6: Find a message with digest starting with "a1" ---
i = 0
while True:
    msg = str(i)
    digest = hashlib.sha256(msg.encode()).hexdigest()
    if digest.startswith("a1"):
        print(f'Message "{msg}" -> digest {digest}  (starts with "a1")')
        break
    i += 1

print("PROBLEM 3: Linked List ")

class huskie:
    def __init__(self, neuID, sport, last_place):
        self.neuID = str(neuID)
        self.sport = str(sport)
        self.last_place = str(last_place)

# One block per group member -- replace with real NEU IDs / sports / places
block1 = huskie("002406382", "Soccer", "California")
block2 = huskie("0024063821", "Basketball", "Boston")
block3 = huskie("0024063812", "Tennis", "Miami")

print("Block 1:", block1.__dict__)
print("Block 2:", block2.__dict__)
print("Block 3:", block3.__dict__)

block1.last_place = "Chicago"      
block2.last_place = "Hawaii"      
block3.last_place = "London"      

print("\nAfter replacing 3rd attribute with 'parents' last place visited':")
print("Block 1:", block1.__dict__)
print("Block 2:", block2.__dict__)
print("Block 3:", block3.__dict__)



print("PROBLEM 4: Blockchain")


class huskies_chain: 
    def __init__(self, blockID, sport, last_place, prevblockhash):
        self.blockID = str(blockID)
        self.sport = str(sport)
        self.last_place = str(last_place)
        self.prevhash = hashlib.sha256(
            json.dumps(prevblockhash).encode("utf-8")
        ).hexdigest()

# Block 1 has no previous block, so set prevhash to "NA"
block1 = huskies_chain("B1", "Soccer", "New York", "NA")
block1.prevhash = "NA"

# Block 2's prevhash is computed from block 1's full info
block2 = huskies_chain("B2", "Basketball", "Boston", block1.__dict__)

# Block 3's prevhash is computed from block 2's full info
block3 = huskies_chain("B3", "Tennis", "Miami", block2.__dict__)

print("Block 1:", block1.__dict__)
print("Block 2:", block2.__dict__)
print("Block 3:", block3.__dict__)
print("\nHash of the last block (block 3):", block3.prevhash)

print("\nNow if team member 2 changes her sport to 'Sarcastaball':")
block2.sport = "Sarcastaball"
# Recompute the hash chain downstream of the change:
new_hash_for_block3 = hashlib.sha256(
    json.dumps(block2.__dict__).encode("utf-8")
).hexdigest()
print("Recomputed hash of block 3 (using tampered block 2):", new_hash_for_block3)
print(f"Original hash of block 3 was:                        {block3.prevhash}")
print("Hashes match:", new_hash_for_block3 == block3.prevhash)
print("""
How to detect tampering: anyone holding the chain simply recomputes the hash of
each block's contents and compares it to the 'prevhash' stored in the next block.
Changing even one character (sport "Basketball" -> "Sarcastaball")  changes the hash. The recomputed hash
no longer matches the hash that block 3 is carrying, which immediately reveals
that block 2 was altered after the chain was built.
""")

print("PROBLEM 5: Merkle Trees")

def h(x):
    """SHA-256 hash of a single transaction string."""
    return hashlib.sha256(x.encode()).hexdigest()

def h2(a, b):
    """SHA-256 hash of two concatenated hex-digest strings (a parent node)."""
    return hashlib.sha256(a.encode() + b.encode()).hexdigest()

# 5.a: transactions 123, 321, 543, 991
tx = ["123", "321", "543", "991"]
leaves = [h(t) for t in tx]
h12 = h2(leaves[0], leaves[1])
h34 = h2(leaves[2], leaves[3])
root1 = h2(h12, h34)
print("\n5.1 Transactions:", tx)
print("    Merkle tree construction:")
print("      hash(tx1), hash(tx2) -> combined into h12")
print("      hash(tx3), hash(tx4) -> combined into h34")
print("      h12, h34 -> combined into the ROOT hash")
print("    Root hash:", root1)

# 5.b: transactions 123, 100, 200, 205
tx2 = ["123", "100", "200", "205"]
leaves2 = [h(t) for t in tx2]
h12b = h2(leaves2[0], leaves2[1])
h34b = h2(leaves2[2], leaves2[3])
root2 = h2(h12b, h34b)
print("\n5.2 Transactions:", tx2)
print("    Root hash:", root2)

# 5.c1: Does transaction "900" belong?
given_root_a = "337fcd855eaea0689e3b3d18b8e4466411c5b7e301ab05bc01cbaa112a01bcef"
leaves3 = [h(t) for t in ["123", "921", "154", "900"]]
left_pair = h2(leaves3[0], leaves3[1])
right_pair = h2(leaves3[2], leaves3[3])
root3 = h2(left_pair, right_pair)
print("\n5.3a Known leaves: 123, 921, 154, and candidate 900. Given root:")
print("     ", given_root_a)
print("     Recomputed root using 900 as the 4th transaction:")
print("     ", root3)
print("     Match:", root3 == given_root_a, "-> transaction 900 DOES belong to the block.")

# 5.c2: Does transaction "833" belong
given_root_b = "ee7981891d9803e89cddd2daee8f8bd0cbf6201523519e43d0e97d969ac479e1"
right_subtree_given = "9e55c7c935d55594807dd1662e2c4be4eaed24cbf376a8f923a479e7108b5416"
left_subtree = h2(h("104"), h("833"))
root_b = h2(left_subtree, right_subtree_given)
print("\n5.3b Known leaf: 104, candidate: 833. Known sibling subtree hash given directly.")
print("     Given root:    ", given_root_b)
print("     Recomputed root using 833:", root_b)
print("     Match:", root_b == given_root_b, "-> transaction 833 DOES belong to the block.")

# 5.c3: Does transaction "902" belong?
given_root_c = "5b79e19d62ae7cfb21e3c309d99d0dbc74da2f3f6dd1941fd2e88266bb6fee2f"
left_subtree_given = "d38939c11aa2d7868a62f02b7fe5f355b1dc87a2dc7ad65e14f0e11a6fabf6b4"
right_subtree = h2(h("800"), h("902"))
root_c = h2(left_subtree_given, right_subtree)
print("\n5.3c Known leaf: 800, candidate: 902. Known sibling subtree hash given directly.")
print("     Given root:    ", given_root_c)
print("     Recomputed root using 902:", root_c)
print("     Match:", root_c == given_root_c, "-> transaction 902 does NOT belong to the block.")