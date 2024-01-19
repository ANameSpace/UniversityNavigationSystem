import matplotlib.pyplot as plt
import networkx as nx

from utils.Data import Data

G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)
nodes = ["1,1,1", 1, 2, 3, 4, 5]

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
edges = [("1,1,1", 2), (1, 3), (2, 3), (2, 4), (3, 5), (5, 5)]

# добавляем информацию в объект графа
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# рисуем граф и отображаем его
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()


class Navigation:
    _instance = None
    _init_already = False

    G = nx.Graph()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not Navigation._init_already:
            self.d = Data()

            self.graph = nx.Graph()
            self.nodes = []
            self.edges = []

            # Load floors
            self.nodes.append(self.d.get_you_pos()[0])
            for floor in self.d.get_floors():
                # load rooms
                for room in self.d.get_rooms(floor):
                    n = str(floor + ".room." + room.getName())

                    self.nodes.append(n)
                    self.graph.add_edge(n, room.getCorridor(), weight=1)

                # load ladders
                for ladder in self.d.get_ladders(floor):
                    n = str(floor + ".ladder." + ladder.getName())
                    self.nodes.append(n)
                    self.graph.add_edge(n, ladder.getCorridor(), weight=1)

                # load corridors
                for corridor in self.d.get_corridors(floor):
                    n = str(floor + ".corridor." + corridor.getName())
                    self.nodes.append(n)
                    #self.edges.append(tuple(n, ladder.))

            self.graph.add_nodes_from(self.nodes)
            self.graph.add_edges_from(self.edges)



            Navigation._init_already = True

    def get_edges(self, end_point):
        return nx.shortest_path(self.graph, self.d.get_you_pos()[0], str(end_point))
