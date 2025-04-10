#hm.py
import hmac
import hashlib

message = "Welcome to AMSPSINGH04."
key = "abracadabra"

# Create HMAC-MD5
hmac_md5 = hmac.new(key=key.encode(), msg=message.encode(), digestmod=hashlib.md5)
message_digest = hmac_md5.hexdigest()

print(f"HMAC-MD5: {message_digest}")

hmac_sha512 = hmac.new(key=key.encode(), msg=message.encode(), digestmod=hashlib.sha512)
message_digest = hmac_sha512.hexdigest()

print(f"HMAC-SHA512: {message_digest}")

hmac_sha256 = hmac.new(key=key.encode(), msg=message.encode(), digestmod=hashlib.sha256)
message_digest = hmac_sha256.hexdigest()

print(f"HMAC-SHA256: {message_digest}")

hmac_sha1 = hmac.new(key=key.encode(), msg=message.encode(), digestmod=hashlib.sha1)
message_digest = hmac_sha1.hexdigest()

print(f"HMAC-SHA1: {message_digest}")