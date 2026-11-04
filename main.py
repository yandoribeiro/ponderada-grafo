import networkx as nx
import matplotlib.pyplot as plt

class Grafo(nx.Graph):
    pass

RA = "510270"
DESTINO = "S7" if int(RA[-1]) % 2 == 0 else "S6"
PESOS = [10, 15, 10, 12, 15, 14, 9, 14, 8, 17, 24, 11, 20]

RAMAIS = [
    ("S0", "S1"), ("S0", "S2"), ("S1", "S2"), ("S1", "S3"),
    ("S2", "S4"), ("S2", "S5"), ("S3", "S4"), ("S3", "S6"),
    ("S4", "S5"), ("S4", "S7"), ("S5", "S7"), ("S6", "S7"),
    ("S1", "S4"),
]

G = Grafo()
G.add_nodes_from([f"S{i}" for i in range(8)])
for (u, v), peso in zip(RAMAIS, PESOS):
    G.add_edge(u, v, weight=peso)

print(f"RA: {RA} | destino: {DESTINO}")
print("Pesos e1–e13:", PESOS)
print("\nMatriz de adjacência (None = -):")
print("     " + "".join(f"{'S' + str(i):>5}" for i in range(8)))
for i in range(8):
    linha = []
    for j in range(8):
        u, v = f"S{i}", f"S{j}"
        valor = G[u][v]["weight"] if G.has_edge(u, v) else "-"
        linha.append(f"{valor:>5}")
    print(f"S{i:<3} " + "".join(linha))

ROTA = nx.dijkstra_path(G, "S0", DESTINO, weight="weight")
CUSTO = nx.dijkstra_path_length(G, "S0", DESTINO, weight="weight")
ANTECESSORES, DISTANCIAS = nx.dijkstra_predecessor_and_distance(
    G, "S0", weight="weight"
)
FECHAMENTO = sorted(DISTANCIAS, key=lambda s: (DISTANCIAS[s], int(s[1:])))
FECHAMENTO = FECHAMENTO[: FECHAMENTO.index(DESTINO) + 1]

print("\nRota ótima:", " -> ".join(ROTA))
print("Custo mínimo:", CUSTO, "km")
print("Ordem de fechamento:", " -> ".join(FECHAMENTO))
print("Antecessores:", {s: ANTECESSORES[s] for s in FECHAMENTO})

AGM = list(nx.minimum_spanning_edges(G, algorithm="prim", weight="weight", data=True))
print("Custo no Prim:", sum(dados["weight"] for _, _, dados in AGM))

POSICOES = {
    "S0": (0, 1), "S1": (1, 2), "S2": (2, 1), "S3": (2, 3),
    "S4": (3, 2), "S5": (4, 1), "S6": (4, 3), "S7": (5, 2),
}
ARESTAS_ROTA = set(zip(ROTA, ROTA[1:])) | set(zip(ROTA[1:], ROTA))

nx.draw_networkx_nodes(G, POSICOES, node_color="lightblue", node_size=900)
nx.draw_networkx_labels(G, POSICOES, font_weight="bold")
nx.draw_networkx_edges(
    G, POSICOES,
    edge_color=["crimson" if (u, v) in ARESTAS_ROTA else "gray" for u, v in G.edges()],
    width=[3 if (u, v) in ARESTAS_ROTA else 1.5 for u, v in G.edges()],
)
nx.draw_networkx_edge_labels(G, POSICOES, edge_labels=nx.get_edge_attributes(G, "weight"))
plt.title(f"Smart Grid - pesos dos ramais (km), rota ótima em vermelho")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafo_smart_grid.png", dpi=200)
plt.show()