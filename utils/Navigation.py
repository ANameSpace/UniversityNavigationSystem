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
            # load file
            self.current_directory = os.getcwd()
            self.logs_directory = os.path.join(self.current_directory, "logs")
            if not os.path.exists(self.logs_directory):
                os.makedirs(self.logs_directory)
            self.log_file = os.path.join(self.logs_directory, self.generate_file_name())

            # add from file
            G.add_edge("A", "B", weight=2)
            G.add_edge("B", "C", weight=1)
            G.add_edge("A", "C", weight=5)

            Navigation._init_already = True

    def get_edges(self, end_point):
        return nx.shortest_path(G, Data().get_you_pos()[0], str(end_point))
