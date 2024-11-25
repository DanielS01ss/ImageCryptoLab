from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

# IV and Ciphertext provided
iv_hex = "aabbccddeeff00998877665544332211"
iv = bytes.fromhex(iv_hex)

plaintext = b'This is a top secret!'

ciphertext_hex = "a1e22d26a8db9a59283ad5782f10a343449f3ed216a4b79c47981cc7dd9221d3"
ciphertext = bytes.fromhex(ciphertext_hex)


def try_decrypt(key):
    
    try: 
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted
    except (ValueError, KeyError):  
        return None


def populate_word_list(file_path):
    """Load the word list from a file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def start_cracking(word_list):
    """Attempt to crack the encryption by trying keys from the word list."""
    for word in word_list:
        # Create a 32-byte key padded with '#' as required
        key = (word + '#' * (32 - len(word))).encode()
        decrypted_text = try_decrypt(key)
        
        if decrypted_text == plaintext:
            print(f"Found the key: {word}")
            break
    else:
        print("Key not found in the word list.")


# Populate word list from the file
word_list = populate_word_list("Lab56_words.txt")

# Ensure the word list is not empty
if word_list:
    start_cracking(word_list)
else:
    print("The word list is empty. Please check the file.")
