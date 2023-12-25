import sys
from networkx import Graph, minimum_edge_cut, connected_components

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    graph = Graph()
    for row in inp:
        l, rs = row.split(': ')
        for r in rs.split(' '):
            graph.add_edge(l, r)
    return graph

def part1(graph):
    cuts = minimum_edge_cut(graph)
    graph.remove_edges_from(cuts)
    disconnected = list(connected_components(graph))
    assert len(disconnected) == 2
    return len(disconnected[0]) * len(disconnected[1])

graph = parse_input(inp)
print('part1:', part1(graph))
