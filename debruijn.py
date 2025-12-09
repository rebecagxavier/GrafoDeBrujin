from collections import defaultdict
from typing import List, Dict, Set

def load_kmers_from_file(path: str) -> List[str]:
    kmers = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            kmers.append(line)
    return kmers

class DeBruijnGraph:
    def __init__(self, kmers: List[str]):
        if not kmers:
            raise ValueError("Empty k-mer list")

        self.k = len(kmers[0])

        for km in kmers:
            if len(km) != self.k:
                raise ValueError("All k-mers must have the same length")

        self.kmers = list(dict.fromkeys(kmers))   # remove duplicados mantendo ordem
        self.nodes = set(self.kmers)

        self.out_edges: Dict[str, Set[str]] = defaultdict(set)
        self.in_edges: Dict[str, Set[str]] = defaultdict(set)

        self._build_edges()

    def _build_edges(self):
        """Cria arestas u -> v quando suffix(u,k-1) == prefix(v,k-1)."""
        k_1 = self.k - 1

        prefix_map = defaultdict(list)
        for node in self.nodes:
            prefix = node[:k_1]
            prefix_map[prefix].append(node)

        for node in self.nodes:
            suffix = node[1:]
            for v in prefix_map.get(suffix, []):  # nós cujo prefixo = meu sufixo
                self.out_edges[node].add(v)
                self.in_edges[v].add(node)

        # garantir que todos tenham entradas no dict
        for n in self.nodes:
            _ = self.out_edges[n]
            _ = self.in_edges[n]

    def indegree(self, node: str) -> int:
        return len(self.in_edges[node])

    def outdegree(self, node: str) -> int:
        return len(self.out_edges[node])

    #extração de unitigs

    def maximal_non_branching_paths(self) -> List[List[str]]:
        paths = []
        visited_edges = set()

        def mark(u, v):
            visited_edges.add((u, v))

        #nós que iniciam caminhos
        for v in self.nodes:
            if self.outdegree(v) > 0 and (self.indegree(v) != 1 or self.outdegree(v) != 1):
                for w in list(self.out_edges[v]):
                    if (v, w) in visited_edges:
                        continue

                    path = [v, w]
                    mark(v, w)

                    # expandir enquanto for nó 1-in 1-out
                    while self.indegree(path[-1]) == 1 and self.outdegree(path[-1]) == 1:
                        nxt = next(iter(self.out_edges[path[-1]]))
                        if (path[-1], nxt) in visited_edges:
                            break
                        path.append(nxt)
                        mark(path[-2], nxt)

                    paths.append(path)

        #ciclos isolados 1-in/1-out
        for v in self.nodes:
            if self.indegree(v) == 1 and self.outdegree(v) == 1:
                w = next(iter(self.out_edges[v]))
                if (v, w) in visited_edges:
                    continue

                cycle = [v, w]
                mark(v, w)

                while True:
                    cur = cycle[-1]
                    nxt = next(iter(self.out_edges[cur]))
                    if (cur, nxt) in visited_edges:
                        break
                    cycle.append(nxt)
                    mark(cur, nxt)
                    if nxt == cycle[0]:
                        break

                if cycle[0] == cycle[-1]:
                    paths.append(cycle[:-1])

        return paths

    def paths_to_sequences(self, paths: List[List[str]]) -> List[str]:
        seqs = []
        for path in paths:
            s = path[0]
            for nxt in path[1:]:
                s += nxt[-1]
            seqs.append(s)
        return seqs

    def export_to_dot(self, filename: str):
        with open(filename, "w") as f:
            f.write("digraph DeBruijnGraph {\n")
            f.write('  rankdir=LR;\n')  # desenhar da esquerda para a direita

            # opcional: nós com forma de caixa
            for node in self.nodes:
                f.write(f'  "{node}" [shape=box];\n')

            # arestas u -> v
            for u in self.nodes:
                for v in self.out_edges[u]:
                    f.write(f'  "{u}" -> "{v}";\n')

            f.write("}\n")

        print(f"Arquivo DOT salvo em: {filename}")

