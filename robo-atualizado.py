import pygame
import time
import random

# Inicializando o pygame
pygame.init()

# Definindo cores
Cores = {
    "BRANCO": (255, 255, 255),
    "PRETO": (0, 0, 0),
    "AZUL": (0, 0, 255),
    "CINZA": (200, 200, 200),
   "VERDE_ESCURO": (0, 128, 0),  # Caminho percorrido
    "VERMELHO": (255, 0, 0)  # Caminho de retorno
}

# Tamanho das células e da matriz
TAMANHO_CELULA = 100
MARGEM = 10  # Reduzimos a margem para facilitar a visualização das linhas

# Função para gerar a matriz aleatória com obstáculos
def gerar_matriz(linhas, colunas, quantidade_obstaculos):
    # Validação da quantidade de obstáculos
    max_obstaculos = linhas * colunas
    if quantidade_obstaculos > max_obstaculos:
        raise ValueError("Quantidade de obstáculos excede a capacidade da matriz.")
    
    # Inicializando a matriz
    matriz = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(0)  # Adiciona 0 para cada célula
        matriz.append(linha)  # Adiciona a linha à matriz

    obstaculos_adicionados = 0
    
    while obstaculos_adicionados < quantidade_obstaculos:
        x, y = random.randint(0, linhas - 1), random.randint(0, colunas - 1)
        if matriz[x][y] == 0:  # Posição livre
            matriz[x][y] = 1  # Coloca um obstáculo
            obstaculos_adicionados += 1  # Incrementa o contador de obstáculos

    return matriz


# Configurações da matriz
LINHAS, COLUNAS, QUANTIDADE_OBSTACULOS = 3, 3, 3
matriz = gerar_matriz(LINHAS, COLUNAS, QUANTIDADE_OBSTACULOS)

# Escolhendo uma posição inicial aleatória para o robô
while True:
    posicao_inicial = (random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1))
    if matriz[posicao_inicial[0]][posicao_inicial[1]] == 0:  # Verifique se a posição é livre
        break

# Definindo a janela do Pygame
LARGURA = COLUNAS * (TAMANHO_CELULA + MARGEM) + MARGEM
ALTURA = LINHAS * (TAMANHO_CELULA + MARGEM) + MARGEM
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Percurso do Robô - DFS")

# Função para desenhar a matriz na tela
def desenhar_matriz(matriz, visitado, caminho_percorrido, caminho_retorno, robo_pos):
    tela.fill(Cores["BRANCO"])
    
    # Desenha a matriz
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            cor = Cores["BRANCO"]
            if matriz[linha][coluna] == 1:
                cor = Cores["PRETO"]  # Obstáculo
            elif (linha, coluna) in caminho_percorrido:
                cor = Cores["VERDE_ESCURO"]  # Caminho percorrido
            elif (linha, coluna) in caminho_retorno:
                cor = Cores["VERMELHO"]  # Caminho de retorno
            elif visitado[linha][coluna]:
                cor = Cores["CINZA"]  # Células já visitadas
            
            # Desenha a célula com borda para criar as linhas visuais
            pygame.draw.rect(tela, cor, [(MARGEM + TAMANHO_CELULA) * coluna + MARGEM,
                                           (MARGEM + TAMANHO_CELULA) * linha + MARGEM,
                                           TAMANHO_CELULA, TAMANHO_CELULA])
            
            # Desenha as linhas da grade (bordas pretas)
            pygame.draw.rect(tela, Cores["PRETO"], [(MARGEM + TAMANHO_CELULA) * coluna + MARGEM,
                                                     (MARGEM + TAMANHO_CELULA) * linha + MARGEM,
                                                     TAMANHO_CELULA, TAMANHO_CELULA], 1)
    
    # Desenha o robô na posição atual
    pygame.draw.rect(tela, Cores["AZUL"], [(MARGEM + TAMANHO_CELULA) * robo_pos[1] + MARGEM,
                                              (MARGEM + TAMANHO_CELULA) * robo_pos[0] + MARGEM,
                                              TAMANHO_CELULA, TAMANHO_CELULA])
    pygame.display.flip()

# Função para verificar se a posição é válida
def eh_valido(x, y, matriz, visitado):
    return 0 <= x < LINHAS and 0 <= y < COLUNAS and matriz[x][y] == 0 and not visitado[x][y]


def dfs_com_retorno(matriz, x, y, visitado, caminho_percorrido, caminho_retorno):
    # Pilha para armazenar o caminho percorrido
    pilha = [(x, y)]
    
    while pilha:
        x, y = pilha[-1]  # Pega o topo da pilha (posição atual)
        visitado[x][y] = True
        caminho_percorrido.append((x, y))
        desenhar_matriz(matriz, visitado, caminho_percorrido, caminho_retorno, (x, y))
        time.sleep(0.3)  # Pausa para visualizar o movimento do robô
        
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, baixo, esquerda, direita
        moveu = False

        # Verifica todas as direções
        for mov in movimentos:
            novo_x, novo_y = x + mov[0], y + mov[1]
            if eh_valido(novo_x, novo_y, matriz, visitado):
                pilha.append((novo_x, novo_y))  # Adiciona a nova posição à pilha
                moveu = True
                break
        
        # Se não conseguiu se mover, significa que o robô está preso
        if not moveu:
            caminho_retorno.append((x, y))  # Adiciona o ponto de retorno ao caminho
            pilha.pop()  # Remove a posição atual da pilha (volta)
            desenhar_matriz(matriz, visitado, caminho_percorrido, caminho_retorno, (x, y))
            time.sleep(0.3)

# Função principal para percorrer a matriz
def percorrer_matriz(matriz, posicao_inicial):
    # Cria uma matriz de booleanos para rastrear as células visitadas
    visitado = []  # Lista para armazenar linhas
    for i in range(LINHAS):
        linha = []  # Lista para armazenar células da linha
        for j in range(COLUNAS):
            linha.append(False)  # Inicializa todas as células como não visitadas
        visitado.append(linha)  # Adiciona a linha à matriz de visitados

    # Lista para armazenar o caminho percorrido pelo robô
    caminho_percorrido = []  
    
    # Lista para armazenar o caminho de retorno do robô
    caminho_retorno = []  
    
    dfs_com_retorno(
        matriz, 
        posicao_inicial[0],  # Coordenada x inicial
        posicao_inicial[1],  # Coordenada y inicial
        visitado,            # Matriz de células visitadas
        caminho_percorrido,  # Caminho percorrido pelo robô
        caminho_retorno      # Caminho de retorno do robô
    )

# Iniciando a simulação
percorrer_matriz(matriz, posicao_inicial)

# Loop principal do pygame
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()
