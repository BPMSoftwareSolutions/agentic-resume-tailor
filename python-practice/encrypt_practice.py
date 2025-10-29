from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(data: bytes) -> bytes:
  padding = 16 - len(data) % 16
  return data + bytes([padding]) * padding

def unpad(data: bytes) -> bytes:
  padding = data[-1]
  return data[:-padding]

def test_padding_cases():
  samples = [b"abcdefghijklmnop", b"abcdefghijklmnopqrstuvwx", b"abcdefghijklmnopqrstuvwxyz"]
  for s in samples:
    padded = pad(s)
    assert len(padded) % 16 == 0
    assert unpad(padded) == s
    unpadded = unpad(padded)
    print("Original:", s)
    print("Length before padding:", len(s))
    print("Length after padding :", len(padded))
    print("Padded data (hex):   ", padded.hex())
    print("Unpadded data (decoded):", unpadded.decode())
    print("Last byte value:     ", padded[-1])
    print("-" * 40)
    print(f"Original: {s} Padded: {padded} Unpadded: {unpadded}")

def encrypt_bill_rate(bill_rate: str, key: bytes) -> str:
  cipher = AES.new(key, AES.MODE_CBC)
  ct_bytes = cipher.encrypt(pad(bill_rate.encode()))
  blob = cipher.iv + ct_bytes
  return base64.b64encode(blob).decode('utf-8')

def decrypt_bill_rate(encrypted_bill_rate: str, key: bytes) -> str:
  raw = base64.b64decode(encrypted_bill_rate)
  iv, ct = raw[:16], raw[16:]
  cipher = AES.new(key, AES.MODE_CBC, iv)
  return unpad(cipher.decrypt(ct)).decode('utf-8')

if __name__ == "__main__":
  test_padding_cases()
