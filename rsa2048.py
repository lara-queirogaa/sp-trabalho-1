import os
import hashlib
import timeit
from cryptography.hazmat.primitives.asymmetric import rsa

#funções auxiliares
def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

#chaves (publica e private), r e r depois de cryptado com rsa(mesmo para todos os files)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

r = os.urandom(32)
r_int = bytes_to_int(r)
rsa_r = pow(r_int, public_key.public_numbers().e, public_key.public_numbers().n)

# Encriptação estilo OAEP simplificado
def encrypt_file(filename):
    with open(filename, "rb") as f:
        m = f.read()

    block_size = 32
    n_blocks = (len(m) + block_size - 1) // block_size
    encrypted_blocks = []

    for i in range(n_blocks):
        block = m[i*block_size:(i+1)*block_size]
        hasher = hashlib.sha256()
        hasher.update(i.to_bytes(4, 'big') + r)
        hash_block = hasher.digest()
        #xor
        cipher_block = bytes(a ^ b for a, b in zip(block, hash_block[:len(block)]))
        encrypted_blocks.append(cipher_block)

    return encrypted_blocks

def decrypt_file(encrypted_blocks):
    decrypted = bytearray()
    for i, cipher_block in enumerate(encrypted_blocks):
        hasher = hashlib.sha256()
        hasher.update(i.to_bytes(4, 'big') + r)
        hash_block = hasher.digest()
        plain_block = bytes(a ^ b for a, b in zip(cipher_block, hash_block[:len(cipher_block)]))
        decrypted.extend(plain_block)
    
    return decrypted

#medição do tempo de execução
def make_encrypt_wrapper(filename):
    return lambda: encrypt_file(filename)

def make_decrypt_wrapper(rsa_r, enc_blocks):
    return lambda: decrypt_file(rsa_r, enc_blocks)

sizes = [8,64,512,4096,32768,262144,2097152]

for size in sizes:
    filename = f"ficheiro_{size}.txt"

    # Encriptação
    encrypt_wrapper = make_encrypt_wrapper(filename)
    rsa_r, enc_blocks = encrypt_file(filename)  # uma vez para pegar os outputs
    encrypt_time = timeit.timeit(encrypt_wrapper, number=3) / 3
    print(f"Encriptação {filename} ({size} bytes): {encrypt_time:.4f} s (média)")

    # Decriptação
    decrypt_wrapper = make_decrypt_wrapper(rsa_r, enc_blocks)
    decrypt_time = timeit.timeit(decrypt_wrapper, number=3) / 3
    print(f"Decriptação {filename} ({size} bytes): {decrypt_time:.4f} s (média)")

    # Verificar correção
    with open(filename, "rb") as f:
        original = f.read()
    decrypted = decrypt_file(rsa_r, enc_blocks)
    assert decrypted == original, "Erro: decriptação falhou!"