import matplotlib.pyplot as plt
import networkx as nx

from app.utils.Data import Data


# G = nx.Graph()  # создаём объект графа
#
# # определяем список узлов (ID узлов)
# nodes = ["1,1,1", 1, 2, 3, 4, 5]
#
# # определяем список рёбер
# # список кортежей, каждый из которых представляет ребро
# # кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
# edges = [("1,1,1", 2), (1, 3), (2, 3), (2, 4), (3, 5), (5, 5)]
#
# # добавляем информацию в объект графа
# G.add_nodes_from(nodes)
# G.add_edges_from(edges)
#
# # рисуем граф и отображаем его
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()


class Navigation:
    _instance = None
    _init_already = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not Navigation._init_already:
            self.d = Data()

            self.graph1 = nx.Graph()
            self.nodes1 = []
            self.edges1 = []

            self.graph2 = nx.Graph()
            self.nodes2 = []
            self.edges2 = []

            # Load floors
            self.graph1.add_node("f1")
            self.graph2.add_node("f2")

            for room in self.d.get_rooms("1"):
                self.graph1.add_node(room.getName())

                self.graph2.add_edge("f1", room.getName(), weight=1)

            for room in self.d.get_rooms("2"):
                self.graph2.add_node(room.getName())

            self.graph1.add_edge("f1", "101", weight=1)

            self.graph1.add_edge("f1", "f1-t-108", weight=1)
            self.graph1.add_edge("f1-t-108", "108", weight=1)

            self.graph1.add_edge("f1-t-108", "f1-t-110-109", weight=1)
            self.graph1.add_edge("f1-t-110-109", "109", weight=1)
            self.graph1.add_edge("f1-t-110-109", "110", weight=1)



            self.graph2.add_edge("f2", "208-207-f2", weight=1)

            self.graph2.add_edge("f2", "200-f2", weight=1)
            self.graph2.add_edge("200-f2", "200", weight=1)

            self.graph2.add_edge("208-207-f2", "207",  weight=1)
            self.graph2.add_edge("208-207-f2", "208", weight=1)

            self.graph2.add_edge("200-f2", "f2-t", weight=1)

            self.graph2.add_edge("f2-t", "f2-t-206", weight=1)
            self.graph2.add_edge("f2-t-206", "206", weight=1)

            self.graph2.add_edge("f2-t-206", "f2-t-203-204", weight=1)
            self.graph2.add_edge("f2-t-203-204", "203", weight=1)
            self.graph2.add_edge("f2-t-203-204", "204", weight=1)

            self.graph2.add_edge("f2-t-203-204", "f2-t-201-202", weight=1)
            self.graph2.add_edge("f2-t-201-202", "201", weight=1)
            self.graph2.add_edge("f2-t-201-202", "202", weight=1)


                #self.graph2.add_edge(n, room.getCorridor(), weight=1)


            Navigation._init_already = True

    def run(self, end_point_name: str, z):
        if z == "2":
            return nx.shortest_path(self.graph2, "f2", str(end_point_name))
        else:
            return nx.shortest_path(self.graph1, "f1", str(end_point_name))
