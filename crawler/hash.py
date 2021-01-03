import hashlib

hash_a = int(hashlib.sha224("a".encode('utf-8')).hexdigest(), 16)
hash_re_a = int(hashlib.sha224("b".encode('utf-8')).hexdigest(), 16)

print(hash_a % (10**9))
print(hash_re_a % (10**9))
