import networkx as nx
import pydot

def load_graphs(dot_file, direct=None):
    if direct == 'Normal':
        G = nx.Graph(nx.nx_pydot.read_dot(dot_file))
    else:
        G = nx.DiGraph(nx.nx_pydot.read_dot(dot_file))

    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0]

    node_list = graph.get_nodes()

    # print(node1.get_name())
    # print(node1.get_label())

    node_dict = {}

    for i in node_list:
        temp_dict = {}
        node_label = i.get_label().strip('"')
        node_name= node_label.strip('{').strip('}')
        temp_dict[i.get_name()] = node_name
        node_dict[i.get_name()] = node_name

        G = nx.relabel_nodes(G, temp_dict)

    print('Finish loading graphs')
    return G, node_dict

def get_successors(G):
    successor_dict = {}

    nodes = list(G.nodes())
    for node in nodes:
        successor_list = list(G.successors(node))
        # successor_list.append(node)
        successor_dict[node] = successor_list
    # print(successor_dict)

    return successor_dict

def get_neighbors(G):
    neighbors_dict = {}

    nodes = list(G.nodes)
    for node in nodes:
        neighbors_list= list(G.neighbors(node))
        neighbors_list.append(node)
        neighbors_dict[node] = neighbors_list

    return neighbors_dict

def traverse_graph():
    # TODO: Traverse
    # all_paths = []
    #
    # roots = (v for v, d in G.in_degree() if d == 0)
    # leaves = [v for v, d in G.out_degree() if d == 0]
    #
    # for root in roots:
    #     paths = nx.all_simple_paths(G, source=root, target=leaves)
    #     all_paths.extend(paths)
    #
    # for i in all_paths:
    #     print(i)
    pass

def test_func(G):

    # Test 1
    print(len(list(G.successors('main'))))

    # Test 2
    print(list(G.nodes))
    print(len(list(G.nodes)))
    print(len(list(set(list(G.nodes)))))

if __name__ == '__main__':
    G, _ = load_graphs('newcallgraph.dot', 'Normal')
    print(get_neighbors(G))
