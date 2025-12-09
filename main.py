from debruijn import load_kmers_from_file, DeBruijnGraph

# Carregar k-mers do arquivo já incluído no repositório
kmers = load_kmers_from_file("kmers.txt")

dbg = DeBruijnGraph(kmers)

# Exportar o grafo
dbg.export_to_dot("graph.dot")
print("Grafo exportado para graph.dot")

# Gerar unitigs
paths = dbg.maximal_non_branching_paths()
unitigs = dbg.paths_to_sequences(paths)

print("\nUnitigs gerados:")
for u in unitigs:
    print(u)

