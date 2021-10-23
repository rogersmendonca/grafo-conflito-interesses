# -*- encoding: utf-8 -*-
"""Módulo busca_ciclos_no_grafo

Módulo Busca Ciclos no Grafo
Busca, por meio da implementacao do Algoritmo de Johnson com a biblioteca igraph, os ciclos em um grafo.

Autor: Rogers Reiche de Mendonça <rogers.rj@gmail.com>
Data: Outubro/2021
"""
from collections import defaultdict
import csv
import sys
import time

import igraph as ig

from common.logging import log

# Constante com o numero minimo de vertices de um SCC (Strong Connected Components) considerado pelo Algoritmo de
# Johnson. Ao utilizar MIN_SCC_SIZE = 2, desconsidera-se os ciclos de 1 vertice (ou seja, autorrelacionamentos).
MIN_SCC_SIZE = 2


def simple_cycles_ig(G: ig.Graph,
                     limit_len: int = -1,
                     limit_node_type: str = None,
                     log_file: str = None):
    """
        Rewrite of simple_cycles function from the networkx library to igraph library.

        This is a nonrecursive, iterator/generator version of Johnson's
        algorithm [1]_.  There may be better algorithms for some cases [2]_ [3]_.

        Parameters
        ----------
        G : igraph.Graph
           A directed graph
        limit_len : int
           Limit count of the nodes in cycle. If -1  (default), cycle length is unlimited.
        limit_node_type : string
           Node type to consider in cycle limit length. If None (default), consider all node types.
        log_file : string
           Log file path.

        Returns
        -------
        cycle_generator: generator
           A generator that produces elementary cycles of the graph.
           Each cycle is represented by a list of nodes along the cycle.

        References
        ----------
        .. [1] Finding all the elementary circuits of a directed graph.
           D. B. Johnson, SIAM Journal on Computing 4, no. 1, 77-84, 1975.
           http://dx.doi.org/10.1137/0204007
        .. [2] Enumerating the cycles of a digraph: a new preprocessing strategy.
           G. Loizou and P. Thanish, Information Sciences, v. 27, 163-182, 1982.
        .. [3] A search strategy for the elementary cycles of a directed graph.
           J.L. Szwarcfiter and P.E. Lauer, BIT NUMERICAL MATHEMATICS,
           v. 16, no. 2, 192-204, 1976.
    """

    def _unblock(thisnode, blocked, B):
        stack = {thisnode}
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()

    def _get_neighbors(subG, node_id):
        return [subG.vs[i]['id']
                for i in subG.neighbors(subG.vs.find(id=node_id), mode='out')]

    def _strongly_connected_components(subG: ig.Graph, min_scc_size: int = 1):
        scc_list = list(subG.components(mode='STRONG'))  # list of list
        scc_list_obj_id = [subG.vs[scc]['id'] for scc in scc_list if
                           len(scc) >= min_scc_size]  # list of list
        return [set(frozenset(scc)) for scc in scc_list_obj_id]  # list of set

    def is_path_in_limit(subG, path, limit_len, limit_node_type):
        if limit_len < 0:
            return True
        elif limit_node_type is None:
            return len(path) <= limit_len
        else:
            node_type_count = 0
            for node_id in path:
                if subG.vs.find(id=node_id)['tipo'] == limit_node_type:
                    node_type_count += 1
                    if node_type_count > limit_len:
                        return False
            return True

    if not (isinstance(G, ig.Graph) and G.is_directed()):
        raise Exception('[simple_cycles_ig] G parameter '
                        'is not a instance of igraph.Graph class.')

    try:
        limit_len = int(limit_len)
    except ValueError:
        raise Exception(f"[simple_cycles_ig] limit '{limit_len}' "
                        f"is not a int type parameter.")

    # Johnson's algorithm requires some ordering of the nodes.
    # We assign the arbitrary ordering given by the strongly connected comps
    # There is no need to track the ordering as each node removed as processed.
    # Also we save the actual graph so we can mutate it. We only take the
    # edges because we do not want to copy edge and node attributes here.
    subG = G.copy()
    subG.vs['id'] = [v.index for v in subG.vs]
    total_vs = len(subG.vs)
    total_es = len(subG.es)
    # sccs = _strongly_connected_components(subG)
    sccs = _strongly_connected_components(subG=subG, min_scc_size=MIN_SCC_SIZE)
    i = 0
    while sccs:
        i += 1
        scc = sccs.pop()

        # order of scc determines ordering of nodes
        startnode = scc.pop()
        # Processing node runs "circuit" routine from recursive version
        path = [startnode]
        blocked = set()  # vertex: blocked from search?
        closed = set()  # nodes involved in a cycle
        blocked.add(startnode)
        B = defaultdict(set)  # graph portions that yield no elementary circuit
        stack = [(startnode, _get_neighbors(subG, startnode))]  # subG gives comp nbrs
        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs and is_path_in_limit(subG, path, limit_len, limit_node_type):
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    log(f"{i}. cycle = {path[:]}", log_file=log_file)
                    yield path[:]
                    closed.update(path)
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append((nextnode, _get_neighbors(subG, nextnode)))
                    closed.discard(nextnode)
                    blocked.add(nextnode)
                    continue
            # done with nextnode... look for more neighbors
            if (not nbrs) or (not is_path_in_limit(subG, path, limit_len, limit_node_type)):
                if thisnode in closed:
                    _unblock(thisnode, blocked, B)
                else:
                    for nbr in _get_neighbors(subG, thisnode):
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
                path.pop()
        # done processing this node
        subG.delete_vertices(subG.vs.find(id=startnode).index)

        scc_subG_id = [subG.vs.find(id=node_id).index for node_id in scc]
        H = subG.subgraph(scc_subG_id)
        scc_extend_list = _strongly_connected_components(H)

        for scc_ext in scc_extend_list:
            if len(scc_ext) >= MIN_SCC_SIZE:
                sccs.extend([scc_ext])
            else:
                subG.delete_vertices([subG.vs.find(id=node_id).index for node_id in scc_ext])

        log(f"{i}. subgraph ("
            f"{len(subG.vs)}/{total_vs} vertices [{(1 - (len(subG.vs) / total_vs)) * 100:.2f}% processed], "
            f"{len(subG.es)}/{total_es} edges [{(1 - (len(subG.es) / total_es)) * 100:.2f}% processed]"
            f")", log_file=log_file)


def search_cycles(csv_edges_input: str,
                  txt_cycles_output: str,
                  cycle_limit_len: int,
                  cycle_limit_node_type: str,
                  log_file: str):
    # Create graph
    csv_edges = open(csv_edges_input, mode='r', encoding='utf-8-sig')
    dict_edges = csv.DictReader(csv_edges, delimiter=';', quoting=csv.QUOTE_NONE)
    graph = ig.Graph.DictList(vertices=None, edges=dict_edges, directed=True)
    graph.vs['tipo'] = [name.split('-')[0] for name in graph.vs['name']]
    log(f"grafo criado ({len(graph.vs)} vertices, {len(graph.es)} edges)", log_file=log_file)

    # Get cycles
    try:
        i = 0
        for cycle in simple_cycles_ig(graph,
                                      cycle_limit_len,
                                      cycle_limit_node_type,
                                      log_file):
            i += 1
            with open(txt_cycles_output, 'a') as fd:
                print(cycle, file=fd)
        log(f"TOTAL = {i} cycles", log_file=log_file)
    except Exception as e:
        log(f"\nException:\n {e} \n", log_file=log_file)


def help():
    print('''
        Uso: python -m busca_ciclos_no_grafo <csv_edges_input> <txt_cycles_output> [<cycle_limit_length> <cycle_limit_node_type>]
        Exemplo: python -m busca_ciclos_no_grafo ./edges.csv ./cycles.txt 8
    ''')


def main():
    if len(sys.argv) < 3:
        help()
        sys.exit(-1)
    else:
        csv_input_edges = sys.argv[1]
        txt_output_cycles = sys.argv[2]
        cycle_limit_len = sys.argv[3] if len(sys.argv) >= 4 else -1
        cycle_limit_node_type = sys.argv[4] if len(sys.argv) >= 5 else None

        log_file = f"{txt_output_cycles}.log"

        log(f"Inicio do processamento", log_file=log_file)
        log(f"csv_input_edges: {csv_input_edges}", log_file=log_file)
        log(f"txt_output_cycles: {txt_output_cycles}", log_file=log_file)
        log(f"cycle_limit_len: {cycle_limit_len}", log_file=log_file)
        log(f"cycle_limit_node_type: {cycle_limit_node_type}", log_file=log_file)

        start = time.time()
        search_cycles(csv_input_edges, txt_output_cycles, cycle_limit_len, cycle_limit_node_type, log_file)
        end = time.time()

        delta = end - start
        mins, secs = divmod(delta, 60)
        hours, mins = divmod(mins, 60)

        log('Processamento concluido!', log_file=log_file)
        log(f"Tempo de execucao: {delta} "
            f"({int(hours):02}:{int(mins):02}:{int(secs):02}.{str(secs - int(secs)).split('.')[1]})",
            log_file=log_file)


if __name__ == "__main__":
    main()
