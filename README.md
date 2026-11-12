# Planejamento de Rotas em Barra do Garças (UCS e A*)

Trabalho da disciplina de **Inteligência Artificial** (Ciência da Computação – UFMT). O programa encontra o caminho mais curto entre dois pontos de Barra do Garças – MT, como um "mini Google Maps", usando o mapa real da cidade extraído do **OpenStreetMap**.

## O problema

O mapa da cidade é modelado como um grafo:

- **Locais**: cada nó do OpenStreetMap, com latitude, longitude e tags (ex.: `amenity=food`).
- **Conexões**: trechos de rua entre dois locais, com a distância em metros (podem ser percorridos nos dois sentidos).
- **Pontos de referência**: lugares conhecidos da cidade (UFMT, Prefeitura, Banco do Brasil, Águas Quentes, Cachoeira da Usina, etc.), definidos em `data/bg-landmarks.json`.

### Parte 1 — Caminho mais curto entre dois pontos (`trab-parte1.py`)

- **Uniform Cost Search** (`ucs.py`): expande sempre o nó de menor custo acumulado `g(n)`.
- **A\*** (`a_start.py`): expande o nó de menor `f(n) = g(n) + h(n)`.
- **Heurística**: distância em linha reta pela fórmula de Haversine. Como nenhum trajeto pelas ruas é menor que a linha reta, a heurística nunca superestima o custo real, ou seja, é **admissível**, e o A\* continua encontrando o caminho ótimo explorando menos estados que a UCS.

### Parte 2 — Rota com pontos de passagem obrigatórios (`trab-parte2.py`)

O caminho precisa passar por um conjunto de locais antes de chegar ao destino (ex.: sair da UFMT, passar pela Igreja Matriz e pelo Flutuante e terminar no Fórum).

Para isso, o **estado** guarda, além da posição atual, o **conjunto de pontos obrigatórios já visitados** (`frozenset`). O objetivo só é atingido quando a posição é o destino **e** todos os pontos foram visitados. Os mesmos algoritmos (UCS e A\*) resolvem o problema sem alteração.

## Como executar

Pré-requisitos: Python 3.10+.

```bash
pip install -r requirements.txt
cd trabalho
python trab-parte1.py   # Banco do Brasil -> Cachoeira da Usina
python trab-parte2.py   # UFMT -> Igreja Matriz + Flutuante -> Fórum
```

O caminho encontrado é impresso no terminal e desenhado sobre o mapa em uma página interativa (Plotly). Para trocar a origem, o destino ou os pontos de passagem, altere as tags no bloco `if __name__ == "__main__":` de cada arquivo (as tags disponíveis estão em `data/bg-landmarks.json`).

## Estrutura

```
trabalho/
├── search_base.py      # classes base: SearchProblem, SearchAlgorithm, Node, State
├── ucs.py              # Uniform Cost Search
├── a_start.py          # A*
├── map_util.py         # leitura do .pbf, construção do grafo, distância de Haversine
├── visualization.py    # desenho do caminho no mapa (Plotly)
├── util.py             # fila de prioridade
├── trab-parte1.py      # problema do caminho mais curto
├── trab-parte2.py      # problema com pontos de passagem
└── data/
    ├── barra-do-garcas.pbf   # mapa da cidade (OpenStreetMap)
    └── bg-landmarks.json     # pontos de referência
pdfs/                   # relatórios com os testes e a discussão dos resultados
```

## Tecnologias

Python · osmium (leitura de dados do OpenStreetMap) · Plotly (visualização)
