import sys
import networkx

inp = list(l.strip() for l in sys.stdin.readlines())

graph = networkx.Graph()
for row in inp:
    l, rs = row.split(': ')
    for r in rs.split(' '):
        graph.add_edge(l, r)
cuts = networkx.minimum_edge_cut(graph)
graph.remove_edges_from(cuts)
disconnected = list(networkx.connected_components(graph))

assert len(disconnected) == 2

print(len(disconnected[0]) * len(disconnected[1]))
