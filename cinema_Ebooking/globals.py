from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from Crypto.Cipher import AES

key = b'mysecretpassword'
cipher = AES.new(key, AES.MODE_EAX)
global_tag = None

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

CRYPTO_KEY = Fernet.generate_key()
CIPHER_SUIT = Fernet(CRYPTO_KEY)