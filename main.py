import heapq
import time
import random
import numpy as np
import os
import psutil
import matplotlib.pyplot as plt
from collections import deque

# Funções auxiliares permanecem inalteradas

def gerar_labirinto(tamanho):
    labirinto = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):
            if (i == 0 and j == 0):
                linha.append('S')
            elif (i == tamanho-1 and j == tamanho-1):
                linha.append('E')
            else:
                linha.append('1' if random.random() > 0.3 else '#')
        labirinto.append(linha)
    return labirinto

def caminho_valido(labirinto):
    inicio = (0, 0)
    fim = (len(labirinto) - 1, len(labirinto) - 1)
    fila = deque([inicio])
    visitados = set()
    visitados.add(inicio)

    while fila:
        x, y = fila.popleft()
        if (x, y) == fim:
            return True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto) and labirinto[nx][ny] != '#' and (nx, ny) not in visitados:
                visitados.add((nx, ny))
                fila.append((nx, ny))

    return False

def gerar_labirinto_valido(tamanho):
    while True:
        labirinto = gerar_labirinto(tamanho)
        if caminho_valido(labirinto):
            return labirinto

def imprimir_labirinto(labirinto):
    for linha in labirinto:
        print(" ".join(linha))

def salvar_passos(nome_arquivo, passos):
    nome_arquivo = sanitizar_nome(nome_arquivo)
    with open(nome_arquivo, "w") as arquivo:
        for passo in passos:
            for linha in passo:
                arquivo.write(" ".join(linha) + "\n")
            arquivo.write("\n" + "-"*20 + "\n\n")

def sanitizar_nome(nome):
    return nome.replace(" ", "_").replace("/", "_")

# Algoritmos

def bfs(labirinto):
    inicio = (0, 0)
    fim = (len(labirinto) - 1, len(labirinto) - 1)
    fila = deque([(inicio, [inicio])])
    visitados = set()
    visitados.add(inicio)
    passos = []
    matriz_atual = [linha.copy() for linha in labirinto]  # Copia do labirinto para atualizar

    while fila:
        (x, y), caminho = fila.popleft()

        # Atualiza a matriz com o caminho atual
        for px, py in caminho:
            if matriz_atual[px][py] == '1':
                matriz_atual[px][py] = '*'
        passos.append([linha.copy() for linha in matriz_atual])

        if (x, y) == fim:
            return caminho, passos

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto) and labirinto[nx][ny] != '#' and (nx, ny) not in visitados:
                visitados.add((nx, ny))
                fila.append(((nx, ny), caminho + [(nx, ny)]))

    return [], passos

def dfs(labirinto):
    inicio = (0, 0)
    fim = (len(labirinto)-1, len(labirinto)-1)
    pilha = [(inicio, [inicio])]
    visitados = set()
    passos = []
    passos_visitados = set()

    while pilha:
        (x, y), caminho = pilha.pop()
        if (x, y) == fim:
            return caminho, passos
        if (x, y) not in visitados:
            visitados.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto) and labirinto[nx][ny] != '#' and (nx, ny) not in visitados:
                    pilha.append(((nx, ny), caminho + [(nx, ny)]))

                    passo_labirinto = [linha.copy() for linha in labirinto]
                    for px, py in caminho:
                        if passo_labirinto[px][py] == '1':
                            passo_labirinto[px][py] = '*'
                    if (tuple(map(tuple, passo_labirinto)) not in passos_visitados):
                        passos.append(passo_labirinto)
                        passos_visitados.add(tuple(map(tuple, passo_labirinto)))
    return [], passos

def astar(labirinto):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    inicio = (0, 0)
    fim = (len(labirinto)-1, len(labirinto)-1)
    heap = [(heuristica(inicio, fim), 0, inicio, [inicio])]
    visitados = set()
    passos = []
    passos_visitados = set()

    while heap:
        _, custo, (x, y), caminho = heapq.heappop(heap)
        if (x, y) == fim:
            # Adiciona o caminho final e todos os passos ao resultado
            matriz_resultado = [linha.copy() for linha in labirinto]
            for px, py in caminho:
                if matriz_resultado[px][py] == '1':
                    matriz_resultado[px][py] = '*'
            passos.append(matriz_resultado)
            return caminho, passos

        if (x, y) not in visitados:
            visitados.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto) and labirinto[nx][ny] != '#' and (nx, ny) not in visitados:
                    novo_caminho = caminho + [(nx, ny)]
                    heuristica_custo = heuristica((nx, ny), fim)
                    heapq.heappush(heap, (custo + 1 + heuristica_custo, custo + 1, (nx, ny), novo_caminho))

                    # Atualiza a matriz do labirinto para o passo atual
                    passo_labirinto = [linha.copy() for linha in labirinto]
                    for px, py in novo_caminho:
                        if passo_labirinto[px][py] == '1':
                            passo_labirinto[px][py] = '*'
                    # Adiciona o passo somente se não estiver registrado
                    if tuple(map(tuple, passo_labirinto)) not in passos_visitados:
                        passos.append(passo_labirinto)
                        passos_visitados.add(tuple(map(tuple, passo_labirinto)))

    return [], passos

def greedy(labirinto):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    inicio = (0, 0)
    fim = (len(labirinto)-1, len(labirinto)-1)
    heap = [(heuristica(inicio, fim), inicio, [inicio])]
    visitados = set()
    passos = []
    passos_visitados = set()

    while heap:
        _, (x, y), caminho = heapq.heappop(heap)
        if (x, y) == fim:
            return caminho, passos
        if (x, y) not in visitados:
            visitados.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto) and labirinto[nx][ny] != '#' and (nx, ny) not in visitados:
                    novo_caminho = caminho + [(nx, ny)]
                    heuristica_custo = heuristica((nx, ny), fim)
                    heapq.heappush(heap, (heuristica_custo, (nx, ny), novo_caminho))

                    # Atualiza a matriz do labirinto para o passo atual
                    passo_labirinto = [linha.copy() for linha in labirinto]
                    for px, py in novo_caminho:
                        if passo_labirinto[px][py] == '1':
                            passo_labirinto[px][py] = '*'
                    if tuple(map(tuple, passo_labirinto)) not in passos_visitados:
                        passos.append(passo_labirinto)
                        passos_visitados.add(tuple(map(tuple, passo_labirinto)))

    return [], passos

# Medir tempo e consumo de memória

def medir_desempenho(funcao, labirinto):
    processo = psutil.Process(os.getpid())
    memoria_inicial = processo.memory_info().rss
    tempo_inicial = time.time()
    caminho, passos = funcao(labirinto)
    tempo_final = time.time()
    memoria_final = processo.memory_info().rss
    tempo_execucao = tempo_final - tempo_inicial
    memoria_consumida = memoria_final - memoria_inicial
    completude = 1 if caminho else 0
    optimalidade = len(caminho) if caminho else float('inf')
    return tempo_execucao, memoria_consumida, completude, optimalidade, passos

# Função principal

def executar_algoritmos():
    tamanho_labirinto = 10
    labirinto = gerar_labirinto_valido(tamanho_labirinto)

    print("Labirinto:")
    imprimir_labirinto(labirinto)

    resultados = {}
    algoritmos = {"BFS": bfs, "DFS": dfs, "A*": astar, "Greedy": greedy}

    for nome, funcao in algoritmos.items():
        tempo, memoria, completude, optimalidade, passos = medir_desempenho(funcao, labirinto)
        resultados[nome] = {
            "tempo": tempo,
            "memoria": memoria,
            "completude": completude,
            "optimalidade": optimalidade,
            "passos": passos
        }
        print(f"{nome}: Tempo = {tempo:.6f}s, Memória = {memoria/1024:.2f}KB, Completude = {completude}, Optimalidade = {optimalidade}")
        salvar_passos(f"{nome}_passos.txt", passos)

    # Gráfico de linhas
    algoritmos = list(resultados.keys())
    tempos = [resultados[nome]["tempo"] for nome in algoritmos]
    memorias = [resultados[nome]["memoria"] for nome in algoritmos]
    completudes = [resultados[nome]["completude"] for nome in algoritmos]
    optimalidades = [resultados[nome]["optimalidade"] for nome in algoritmos]

    plt.figure(figsize=(14, 8))

    plt.subplot(2, 2, 1)
    plt.plot(algoritmos, tempos, marker='o', color='b')
    plt.title("Tempo de Execução")
    plt.ylabel("Tempo (s)")

    plt.subplot(2, 2, 2)
    plt.plot(algoritmos, [mem / 1024 for mem in memorias], marker='o', color='r')
    plt.title("Consumo de Memória")
    plt.ylabel("Memória (KB)")

    plt.subplot(2, 2, 3)
    plt.plot(algoritmos, completudes, marker='o', color='g')
    plt.title("Completude")
    plt.ylabel("Completude (1 ou 0)")

    plt.subplot(2, 2, 4)
    plt.plot(algoritmos, optimalidades, marker='o', color='m')
    plt.title("Optimalidade")
    plt.ylabel("Caminho (menor é melhor)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    executar_algoritmos()
