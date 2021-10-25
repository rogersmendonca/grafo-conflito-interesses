# Grafo Direcionado (Busca de Ciclos)
Implementação do [Algoritmo de Johnson](https://www.cs.tufts.edu/comp/150GA/homeworks/hw1/Johnson%2075.PDF), com a biblioteca igraph do Python, para identificar todos os ciclos existentes em um grafo direcionado.

Código fonte utilizado no trabalho **"Conflito de Interesses (Lei 12.813/2013): Contratos, Parentes e Grafos"**, apresentado no [7º Seminário Internacional sobre Análise de Dados na Administração Pública](https://brasildigital.gov.br), em 22/10/2021 ([Vídeo da Apresentação no YouTube](https://youtu.be/1E8XQG6crtg?t=3116)).

## Linha de Comando
`python -m busca_ciclos_no_grafo <csv_edges_input> <txt_cycles_output> [<cycle_limit_length> <cycle_limit_node_type>]`

#### csv_edges_input
[INPUT] Caminho do arquivo CSV das arestas do grafo (mais informações sobre o conteúdo do arquivo abaixo).

#### txt_cycles_output
[OUTPUT] Caminho do arquivo TXT com os ciclos identificados.

#### cycle_limit_length
[OPCIONAL] Número limite de vértices do ciclo. Caso não seja informado, serão buscados ciclos de qualquer tamanho.

#### cycle_limit_node_type
[OPCIONAL] Tipo do vértice a ser considerado na contagem do "cycle_limit_length". Caso não seja informado, serão considerados vértices de qualquer tipo.

### Exemplos
`python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt`

`python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt 8`

`python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt 2 C`

## Biblioteca Python requerida:
* igraph

**Observação:** O arquivo [sample.csv](notebook/sample.csv) é uma **amostra do CSV** das arestas do grafo, a partir de dados simulados.

