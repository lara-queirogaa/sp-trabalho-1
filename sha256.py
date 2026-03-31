import hashlib
import statistics
import timeit
import matplotlib.pyplot as plt

sizes = [8,64,512,4096,32768,262144,2097152]

def sha256_hash(data):
    return hashlib.sha256(data).digest()

# listas para guardar médias e desvios
sha_mean_list = []
sha_std_list = []

repeats = 30 

for s in sizes:
    with open(f"text_files/ficheiro_{s}.txt","rb") as f:
        data = f.read()

    # mede várias vezes
    times = timeit.repeat(lambda: sha256_hash(data), repeat=repeats, number=1)

    # converte para microsegundos
    times_us = [t*1e6 for t in times]

    sha_mean_list.append(statistics.mean(times_us))
    sha_std_list.append(statistics.stdev(times_us))

def run_sha():
    return sizes, sha_mean_list, sha_std_list

def plot_sha():
    plt.figure(figsize=(10,6))

    # Plot com barras de erro
    plt.errorbar(sizes, sha_mean_list, yerr=sha_std_list, marker='o', linestyle='-', label="SHA-256")

    # Escala log no eixo X
    plt.xscale("log")
    plt.xticks(sizes, sizes)  # marca explicitamente os 7 tamanhos

    # Adiciona valores acima de cada ponto
    for x, y in zip(sizes, sha_mean_list):
        plt.text(x, y*1.02, f"{int(y)}", ha='center', va='bottom', fontsize=8)

    plt.xlabel("File size (bytes)")
    plt.ylabel("Time (microseconds)")
    plt.title("SHA-256 Performance")
    plt.grid(True, which="both", linestyle='--', alpha=0.6)
    plt.legend()
    plt.savefig("plots/sha256_performance.png", dpi=300)
    plt.show()