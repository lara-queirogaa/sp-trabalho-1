from aes import run_aes, plot_aes
from rsa2048 import run_rsa, plot_rsa
from sha256 import run_sha, plot_sha

print("Running AES...")
run_aes()
plot_aes()

print("Running RSA...")
run_rsa()
plot_rsa()

print("Running SHA-256...")
run_sha()
plot_sha()

print("Running comparisons...")
import aes_vs_rsa
import aes_vs_sha256
