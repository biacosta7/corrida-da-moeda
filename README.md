🪙 Corrida da Moeda — Descrição do Jogo

Corrida da Moeda é um jogo estatístico interativo que simula, em tempo real, o comportamento de eventos aleatórios. Nele, dois personagens competem em uma corrida cuja progressão depende exclusivamente de lançamentos de moeda. A cada rodada, um lançamento determina o movimento: cara faz o personagem avançar e coroa o mantém parado.

O objetivo do jogo é mostrar, de forma visual e dinâmica, como resultados aleatórios se comportam ao longo do tempo e como eles se aproximam das probabilidades teóricas esperadas.

📊 Conceitos Estatísticos

A dinâmica do jogo é baseada na Distribuição Binomial com probabilidade p = 0.5 (moeda justa). Cada lançamento é um experimento independente com dois resultados possíveis:

Sucesso (1): o personagem avança — equivalente a “cara”.

Fracasso (0): o personagem permanece no lugar — equivalente a “coroa”.

Ao longo das rodadas, o jogo apresenta:

Distribuição empírica: frequência real de caras e coroas observadas em tempo real.

Distribuição teórica: curva esperada da distribuição binomial, podendo também ser aproximada pela distribuição normal conforme o número de lançamentos aumenta.

Essa comparação entre teoria e prática permite visualizar conceitos como variabilidade, Lei dos Grandes Números e convergência estatística de um jeito simples e intuitivo.

# Como rodar

1. Crie uma venv  
```bash
python -m venv venv
```

2. Abra a venv (Windows)  
```bash
venv\Scripts\activate
```

3. Baixe os imports  
```bash
pip install -r requirements.txt
```

4. Rode o jogo  
```bash
python jogo/main.py
```

