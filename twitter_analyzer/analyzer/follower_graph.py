import networkx as nx

from matplotlib import pyplot as plt


if __name__ == '__main__':
    graf = nx.Graph()
    for x in range(1, 100):
        # graf.add_edges_from([(x, x + 1)])
        graf.add_edges_from([(x, x // 10)])

    A = graf.edges()
    for a in A:
        if 5 in a:
            print(a)

    B = nx.to_dict_of_lists(graf)
    print(B[5])

    plt.figure(figsize=(20, 9))
    nx.draw_networkx(graf)
    plt.show()
