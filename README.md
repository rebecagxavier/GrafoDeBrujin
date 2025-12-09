
# Grafo de De Bruijn

Este repositório apresenta uma implementação didática do Grafo de De Bruijn em Python. O objetivo é demonstrar, de forma clara e simplificada, como k-mers podem ser conectados por sobreposições de k−1 caracteres e compactados em sequências maiores (unitigs). Esta implementação prioriza compreensão conceitual, não desempenho.

O repositório inclui:

* `debruijn.py` — implementação da estrutura do grafo;
* `main.py` — script principal de execução;
* `kmers.txt` — arquivo de entrada com k-mers, um por linha.

---

## Como executar

Com Python 3 instalado, execute no terminal:

```bash
python main.py
```
## Visualização do grafo

Para converter o arquivo DOT em imagem (requer Graphviz):

```bash
dot -Tpng graph.dot -o graph.png
```

Alternativamente, o arquivo DOT pode ser aberto em visualizadores online de Graphviz.

---

## Descrição  do funcionamento

1. **Construção do grafo**
   Cada k-mer é tratado como um nó. Arestas dirigidas são adicionadas entre dois k-mers sempre que o sufixo do primeiro (k−1 caracteres) coincide com o prefixo do segundo.

2. **Identificação de caminhos não ramificados**
   Caminhos são iniciados em vértices cujo grau de entrada ou saída difere de 1. A partir deles, percorrem-se sucessores enquanto o vértice atual tiver exatamente um predecessor e um sucessor, caracterizando trechos lineares do grafo.

3. **Compactação (unitigs)**
   Cada caminho é transformado em uma única sequência. O primeiro k-mer é mantido integralmente, e para cada k-mer subsequente adiciona-se apenas seu último caractere, aproveitando a sobreposição natural entre eles.
