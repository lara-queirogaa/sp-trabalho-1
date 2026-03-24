import os
import hashlib
import timeit
import statistics
from cryptography.hazmat.primitives.asymmetric import rsa
import matplotlib.pyplot as plt

#funções auxiliares
def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

#chaves RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

#encriptação e decriptação
def encrypt_file(filename, r):
    with open(filename, "rb") as f:
        m = f.read()

    block_size = 32
    encrypted_blocks = []

    for i in range((len(m) + block_size - 1) // block_size):
        block = m[i*block_size:(i+1)*block_size]

        hasher = hashlib.sha256()
        hasher.update(i.to_bytes(4, 'big') + r)
        hash_block = hasher.digest()

        cipher_block = bytes(a ^ b for a, b in zip(block, hash_block[:len(block)]))
        encrypted_blocks.append(cipher_block)

    return encrypted_blocks

def decrypt_file(encrypted_blocks, r):
    decrypted = bytearray()

    for i, cipher_block in enumerate(encrypted_blocks):
        hasher = hashlib.sha256()
        hasher.update(i.to_bytes(4, 'big') + r)
        hash_block = hasher.digest()

        plain_block = bytes(a ^ b for a, b in zip(cipher_block, hash_block[:len(cipher_block)]))
        decrypted.extend(plain_block)

    return decrypted

#wrappers
def make_encrypt_wrapper(filename, r):
    return lambda: encrypt_file(filename, r)

def make_decrypt_wrapper(enc_blocks, r):
    return lambda: decrypt_file(enc_blocks, r)

sizes = [8,64,512,4096,32768,262144,2097152]

encrypt_mean_list = []
encrypt_std_list = []
decrypt_mean_list = []
decrypt_std_list = []

repeats = 30

for size in sizes:
    filename = f"text_files/ficheiro_{size}.txt"

    #gerar novo r para cada ficheiro
    ###PERGUNTAR AO STOR SE SE FAZ UM PARA CADA OU UM IGUAL PARA TODOS!!!!!!!!!1
    r = os.urandom(32)
    r_int = bytes_to_int(r)
    rsa_r = pow(r_int,
                public_key.public_numbers().e,
                public_key.public_numbers().n)
    
    #wrappers
    encrypt_wrapper = make_encrypt_wrapper(filename, r)

    #encriptar uma vez para obter blocos
    enc_blocks = encrypt_file(filename, r)

    #medir encriptação
    encrypt_times = timeit.repeat(encrypt_wrapper, repeat=repeats, number=1)
    encrypt_times_us = [t*1e6 for t in encrypt_times]

    encrypt_mean = statistics.mean(encrypt_times_us)
    encrypt_std = statistics.stdev(encrypt_times_us)
    #print(f"Encriptação {filename}: {encrypt_mean:.2f} ± {encrypt_std:.2f} μs")

    #medir decriptação
    decrypt_wrapper = make_decrypt_wrapper(enc_blocks, r)

    decrypt_times = timeit.repeat(decrypt_wrapper, repeat=repeats, number=1)
    decrypt_times_us = [t*1e6 for t in decrypt_times]

    decrypt_mean = statistics.mean(decrypt_times_us)
    decrypt_std = statistics.stdev(decrypt_times_us)
    #print(f"Decriptação {filename}: {decrypt_mean:.2f} ± {decrypt_std:.2f} μs")

    #verificação
    with open(filename, "rb") as f:
        original = f.read()

    decrypted = decrypt_file(enc_blocks, r)
    assert decrypted == original, "Erro!"
    encrypt_mean_list.append(encrypt_mean)
    encrypt_std_list.append(encrypt_std)
    decrypt_mean_list.append(decrypt_mean)
    decrypt_std_list.append(decrypt_std)

def run_rsa():
    return sizes, encrypt_mean_list, encrypt_std_list, decrypt_mean_list, decrypt_std_list

def plot_rsa():
    plt.figure(figsize=(10,6))

    # plot com barras de erro
    plt.errorbar(sizes, encrypt_mean_list, yerr=encrypt_std_list,
                marker='o', linestyle='-', label="Encryption")

    plt.errorbar(sizes, decrypt_mean_list, yerr=decrypt_std_list,
                marker='o', linestyle='-', label="Decryption")

    # escala log no eixo X
    plt.xscale("log")
    plt.xticks(sizes, sizes)

    # adicionar valores acima dos pontos
    for x, y in zip(sizes, encrypt_mean_list):
        plt.text(x, y*1.02, f"{int(y)}", ha='center', va='bottom', fontsize=8)

    for x, y in zip(sizes, decrypt_mean_list):
        plt.text(x, y*1.02, f"{int(y)}", ha='center', va='bottom', fontsize=8)

    plt.xlabel("File size (bytes)")
    plt.ylabel("Time (microseconds)")
    plt.title("RSA performance")
    plt.legend()
    plt.grid(True, which="both", linestyle='--', alpha=0.6)

    plt.savefig("plots/rsa_performance.png", dpi=300)
    plt.show()
