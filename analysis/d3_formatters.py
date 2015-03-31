class ForceLayout(object):

    def __init__(self):
        return

    def create_bigrams_graph(bigrams):
        nodes = []
        edges = []
        location = {}
        for a, b in bigrams:
            if a not in location:
                nodes.append({'word': a})
                location[a] = len(nodes) - 1
            if b not in location:
                nodes.append({'word': b})
                location[b] = len(nodes) - 1
            edge = {'source': location[a], 'target' : location[b]}
            edges.append(edge)
        return (nodes, edges)