from aes import run_aes
from rsa2048 import run_rsa
import matplotlib.pyplot as plt

# ir buscar os dados
sizes, aes_enc_mean, aes_enc_std, _, _ = run_aes()
_, rsa_enc_mean, rsa_enc_std, _, _ = run_rsa()

plt.figure(figsize=(10,6))

# AES encryption
plt.errorbar(
    sizes, aes_enc_mean,
    yerr=aes_enc_std,
    marker='o', linestyle='-',
    label="AES Encryption"
)

# RSA encryption
plt.errorbar(
    sizes, rsa_enc_mean,
    yerr=rsa_enc_std,
    marker='o', linestyle='-',
    label="RSA-2048 Encryption"
)

# escala log no eixo X
plt.xscale("log")
plt.xticks(sizes, sizes)

# valores nos pontos (AES)
for x, y in zip(sizes, aes_enc_mean):
    plt.text(x, y*1.02, f"{int(y)}", ha='center', va='bottom', fontsize=8)

# valores nos pontos (RSA)
for x, y in zip(sizes, rsa_enc_mean):
    plt.text(x, y*1.02, f"{int(y)}", ha='center', va='bottom', fontsize=8)

plt.xlabel("File size (bytes)")
plt.ylabel("Time (microseconds)")
plt.title("AES vs RSA-2048 Encryption Performance")
plt.grid(True, which="both", linestyle='--', alpha=0.6)
plt.legend()

plt.savefig("plots/aes_vs_rsa2048.png", dpi=300)
plt.show()