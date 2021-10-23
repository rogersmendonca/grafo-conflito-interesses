# Conflito de Interesses: Contratos, Parentes e Grafos
Busca, por meio da implementação do Algoritmo de Johnson com a biblioteca igraph, os ciclos em um grafo.

Trabalho apresentado no [7º Seminário Internacional sobre Análise de Dados na Administração Pública](https://brasildigital.gov.br), em 22/10/2021 ([Vídeo da Apresentação no YouTube](https://youtu.be/1E8XQG6crtg?t=3116)).

## Linha de Comando
`python -m busca_ciclos_no_grafo <csv_edges_input> <txt_cycles_output> [<cycle_limit_length> <cycle_limit_node_type>]`

#### csv_edges_input
[INPUT] Caminho do arquivo CSV das arestas do grafo (mais informações sobre o conteúdo do arquivo abaixo).

#### txt_cycles_output
[OUTPUT] Caminho do arquivo TXT com os ciclos identificados.

#### cycle_limit_length
[OPCIONAL] Tamanho limite do ciclo. Caso não seja informado, serão buscados todos os ciclos.

#### cycle_limit_node_type
[OPCIONAL] Tipo do vértice a ser considerado na contagem do tamanho limite do ciclo. Caso não seja informado, serão considerados vértices de qualquer tipo.

### Exemplos
python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt

python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt 8

python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt 2 C

## Biblioteca Python requerida:
* igraph

## Arquivo CSV das arestas do grafo (informado no parâmetro **<csv_edges_input>**)

### Arquivo CSV com 3 colunas
* **source** = Nome do vértice de origem
* **target** = Nome do vértice de destino
* **tipo** = Rótulo do tipo do relacionamento

### Padrão para o nome do vértice
O nome do vértice segue o padrão `<1>-<2>`, onde:

* **<1>** = Rótulo do tipo do objeto representado no vértice. Por exemplo: **E** (Empregado); **C** (Contrato); **F** (Fornecedor); **S** (Sócio); **T** (Terceiro)

* **<2>** = Identificador do objeto representado no vértice.

**Observação:** O arquivo [sample.csv](notebook/sample.csv) é uma **amostra do CSV** das arestas do grafo, a partir de dados simulados.

