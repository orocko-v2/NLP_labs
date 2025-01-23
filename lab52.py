import networkx
import matplotlib

import lab5

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

nodes = lab5.nodes
edges = lab5.edges
nx_colormap = plt.colormaps['brg']
graph = networkx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
node_colors = [nx_colormap(node[1]['id']) for node in nodes]
node_labels = networkx.get_node_attributes(graph, 'entity')
edge_labels = networkx.get_edge_attributes(graph, 'label')
pos = networkx.kamada_kawai_layout(graph)
nx_options = {
'font_size': .5,
'labels': node_labels,
'node_size': 10,
'node_color': node_colors,
'width': .4,
'with_labels': True
}

fig = plt.figure(figsize=(30, 30), dpi=500)
networkx.draw_kamada_kawai(graph, **nx_options)
networkx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=.5)
plt.show()
