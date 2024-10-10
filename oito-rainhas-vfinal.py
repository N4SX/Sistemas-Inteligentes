import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque

# Função para plotar o tabuleiro com as rainhas
def plot_tabuleiro(positions, title="Tabuleiro"):
    """
    Esta função desenha o tabuleiro 8x8 e posiciona as rainhas de acordo com 'positions'.
    Cada rainha é representada pela letra 'R' vermelha em um tabuleiro de xadrez padrão.
    """
    fig, ax = plt.subplots()  # Cria uma figura e um eixo para o gráfico
    ax.set_title(title)  # Define o título da figura

    # Cria o tabuleiro de xadrez com casas alternadas (brancas e pretas)
    board = np.zeros((8, 8))  # Inicializa o tabuleiro como uma matriz 8x8 de zeros
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                board[i, j] = 1  # Define as casas brancas (valores 1)
            else:
                board[i, j] = 0  # Define as casas pretas (valores 0)

    # Mostra o tabuleiro com um esquema de cores cinza (0 = preto, 1 = branco)
    ax.imshow(board, cmap='gray')

    # Posiciona as rainhas no tabuleiro, com a letra 'R' em vermelho
    for pos in positions:
        ax.text(pos[1], pos[0], 'R', ha='center', va='center', color='red', fontsize=30, fontweight='bold')

    plt.xticks([])  # Remove os números dos eixos X
    plt.yticks([])  # Remove os números dos eixos Y
    plt.show()  # Exibe o tabuleiro

# Função para gerar posições aleatórias das rainhas
def gerar_posicoes_aleatorias():
    """
    Gera uma configuração aleatória inicial de rainhas.
    Coloca uma rainha em cada linha, mas em colunas aleatórias.
    """
    posicoes = []
    for i in range(8):
        # Gera uma posição aleatória para cada linha do tabuleiro
        posicoes.append((i, random.randint(0, 7)))  # Cada rainha em uma linha diferente
    return posicoes

# Função para verificar se duas rainhas se atacam
def se_atacam(pos1, pos2):
    """
    Verifica se duas rainhas, localizadas nas posições 'pos1' e 'pos2', se atacam.
    Duas rainhas se atacam se estiverem na mesma linha, coluna ou diagonal.
    """
    # Verifica se estão na mesma linha (pos1[0] == pos2[0])
    # Verifica se estão na mesma coluna (pos1[1] == pos2[1])
    # Verifica se estão na mesma diagonal (diferença entre as linhas é igual à diferença entre as colunas)
    return pos1[0] == pos2[0] or pos1[1] == pos2[1] or abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1])

# Função para verificar se o tabuleiro é seguro (não há ataques)
def eh_seguro(positions):
    """
    Verifica se uma configuração de rainhas é segura, ou seja, se nenhuma rainha ataca outra.
    """
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            # Verifica se a rainha na posição i e na posição j se atacam
            if se_atacam(positions[i], positions[j]):
                return False  # Se alguma rainha ataca outra, a configuração não é segura
    return True  # Se não houver ataques, a configuração é segura

# Função para resolver o problema das 8 rainhas com busca em largura, gerando todas as soluções
def bfs_resolver_8_rainhas():
    """
    Utiliza a busca em largura (BFS) para encontrar todas as soluções do problema das 8 rainhas.
    Retorna uma lista contendo todas as soluções válidas.
    """
    fila = deque([[]])  # Inicializa a fila com uma lista vazia (tabuleiro vazio)
    solucoes = []  # Lista que armazenará todas as soluções encontradas
    
    # Enquanto houver estados para explorar na fila
    while fila:
        state = fila.popleft()  # Remove o primeiro estado da fila
        if len(state) == 8:
            # Se o estado tem 8 rainhas e é seguro, então é uma solução
            if eh_seguro(state):
                solucoes.append(state)  # Adiciona a solução à lista de soluções
        else:
            # Expande o estado atual, adicionando rainhas em colunas possíveis
            for col in range(8):
                novo_estado = state + [(len(state), col)]  # Adiciona uma nova rainha na próxima linha
                if eh_seguro(novo_estado):  # Se o novo estado for seguro, adiciona à fila
                    fila.append(novo_estado)
    
    return solucoes  # Retorna todas as soluções encontradas

# Passo 1: Gerar e plotar tabuleiro com rainhas aleatórias
posicoes_aleatorias = gerar_posicoes_aleatorias()
plot_tabuleiro(posicoes_aleatorias, title="Tabuleiro Aleatório")

# Passo 2: Resolver o problema das 8 rainhas usando BFS e encontrar todas as soluções
todas_solucoes = bfs_resolver_8_rainhas()

# Passo 3: Mostrar todas as soluções encontradas
print(f"Total de soluções encontradas: {len(todas_solucoes)}")

# Itera por todas as soluções encontradas e as plota uma a uma
for idx, solucao in enumerate(todas_solucoes):
    plot_tabuleiro(solucao, title=f"Solução {idx+1}")