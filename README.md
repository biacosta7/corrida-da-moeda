# 🪙 Corrida da Moeda (Coin Race)

## 🌟 Visão Geral do Jogo

**Corrida da Moeda** é uma simulação interativa baseada em Pygame que funde um jogo de tabuleiro competitivo com a visualização em tempo real de conceitos de probabilidade.

Quatro jogadores competem para ser o primeiro a **depositar todas as suas moedas** em um cofre central. A progressão de cada jogador é determinada exclusivamente pelo lançamento de uma moeda:

| Resultado | Ação do Jogador |
| :---: | :--- |
| **Cara (C)** | Avança um passo no caminho em direção ao cofre central. |
| **Coroa (K)** | Permanece parado. |

## 📊 O Conceito Estatístico: Lei dos Grandes Números

Embora o resultado de cada lançamento da moeda seja imprevisível, o gráfico demonstra que, a longo prazo, a frequência de obtenção de Cara se estabiliza.

A **Lei dos Grandes Números** afirma que, à medida que o $N$ (Número Total de Lançamentos) aumenta, a **Frequência Relativa** observada dos resultados converge e se aproxima da **Probabilidade Teórica** esperada (neste caso, $0.5$).

### Estrutura do Gráfico

O gráfico rastreia a **frequência relativa de 'Cara'** ao longo dos lançamentos:

| Elemento | Descrição |
| :--- | :--- |
| **Eixo Y** | **Frequência de Caras** (valor de $0$ a $1$). |
| **Eixo X** | **Número Total de Lançamentos** (o número de cliques). |
| **Linha Azul** | Representa a **Frequência Relativa** observada dos resultados Cara. |
| **Linha Tracejada (0.5)** | Representa a **Probabilidade Teórica** de obter Cara ($p=0.5$). |

$$\text{Frequência Observada} \to 0.5, \text{ quando } N \to \infty$$

-----

## 🚀 Como Rodar o Jogo
1. **Clone o reppositório**
   ```bash
   git clone https://github.com/biacosta7/corrida-da-moeda.git
   ```

2.  **Crie um Ambiente Virtual (`venv`):**

    ```bash
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual:**

    ```bash
    venv\Scripts\activate (Windows)
    ```

   ```bash
    source venv/bin/activate (Linux/macOS)
   ```

4.  **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute o Jogo:**

    ```bash
    python jogo/main.py
    ```
