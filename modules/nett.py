import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Crear un grafo
G = nx.Graph()

# Agregar nodos y aristas
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), (3, 7), (2, 5), (6, 8), (8, 9)])


# Definir el layout en 3D
pos = nx.spring_layout(G, dim=3)

# Obtener las posiciones de los nodos en 3D
pos_3d = nx.spring_layout(G, dim=3)

# Dibujar el grafo en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extraer las coordenadas x, y, z de los nodos
x = [pos_3d[node][0] for node in G.nodes()]
y = [pos_3d[node][1] for node in G.nodes()]
z = [pos_3d[node][2] for node in G.nodes()]

# Dibujar nodos
ax.scatter(x, y, z, c='skyblue', s=1000, edgecolors='black')

# Dibujar aristas
for u, v in G.edges():
    ax.plot([pos_3d[u][0], pos_3d[v][0]], [pos_3d[u][1], pos_3d[v][1]], [pos_3d[u][2], pos_3d[v][2]], c='black', linewidth=2)

# Configuraciones adicionales del gráfico
ax.set_axis_off()  # Ocultar los ejes

# Mostrar el grafo
plt.title("Grafo en 3D")
plt.show()
