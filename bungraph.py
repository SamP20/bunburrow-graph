import graphviz

graph = graphviz.Graph("bunny-graph")
graph.attr(rankdir='TB')
graph.attr(ranksep="2")

pairs = [tuple(bun.strip() for bun in line.split("x")) for line in open("all_buns.txt")]

try:
    acquired_pairs = set(tuple(bun.strip() for bun in line.split("x")) for line in open("my_buns.txt"))
except FileNotFoundError:
    acquired_pairs = set()

levels = []

def get_level_depth(bun):
    # Extract the level depth from the bunnny string and convert to zero based index
    _, level, _ = bun.split("-")
    return int(level)-1

def sort_node(bun):
    # Sort the bunnies according to their level depth
    level_depth = get_level_depth(bun)

    while level_depth >= len(levels):
        levels.append(set())

    level_group = levels[level_depth]

    level_group.add(bun)


for a, b in pairs:
    sort_node(a)
    sort_node(b)


for level_group in levels:
    with graph.subgraph() as s:
        s.attr(rank='same')
        for bun in level_group:
            s.node(bun)

for a, b in pairs:
    la, lb = get_level_depth(a), get_level_depth(b)

    color="black"

    if (a,b) in acquired_pairs:
        color="green"
    if la>lb:
        graph.edge(b, a,  color=color)
    else:
        graph.edge(a, b,  color=color)


graph.view()