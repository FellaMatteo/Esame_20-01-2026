import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._artists_list = []
        self.load_all_artists()

        self.nodi = []

        self.best_path = []
        self.best_score = 0


    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        pass

    def build_graph(self, n_min_album):
        # Nodi
        self.nodi = DAO.get_artisti_filtrati(n_min_album)
        for nodo in self.nodi:
            self.G.add_node(nodo)
        print("Nodi creati correttamente.")

        # Archi
        connessioni = DAO.get_connesioni()
        id_map = {a.id : a for a in self.nodi}

        for a1, a2, peso in connessioni:
            if a1 in id_map and a2 in id_map:
                n1 = id_map[a1]
                n2 = id_map[a2]
                self.G.add_edge(n1, n2, weight=peso)

        print("Archi pesati creti con successo.")


    def get_g_details(self):
        n_nodi = self.G.number_of_nodes()
        n_archi = self.G.number_of_edges()

        return n_nodi, n_archi

    def get_neighbors(self, artista_scelto):
        id_map = {a.id: a for a in self.nodi}
        lista_vicino_peso = []

        vicini = self.G.neighbors(id_map[artista_scelto])

        for v in vicini:
            peso = self.G[id_map[artista_scelto]][v]['weight']
            lista_vicino_peso.append((v, peso))

        return sorted(lista_vicino_peso, key=lambda x: x[1])

    def get_best_path(self, artista_scelto, n_art, d_min):
        self.best_path = []
        self.best_score = 0

        self._nodi_validi = DAO.get_art_validi(d_min)

        id_map = {a.id: a for a in self.G.nodes}
        parziale = [id_map[artista_scelto]]

        self.ricorsione(parziale, n_art)
        return self.best_path, self.best_score

    def ricorsione(self, parziale, n_art):

        if len(parziale) > 1:
            peso = self._get_score(parziale)
        else:
            peso = 0

        #1. Ho fatto meglio di prima?
        if peso > self.best_score and len(parziale) == n_art:
            self.best_score = peso
            self.best_path = list(parziale)
            print("Ricorsione conclusa")

        ultimo = parziale[-1]
        #2. Che nodi posso esplorare?
        for nodo in self._nodi_validi:
            if nodo in self.G.neighbors(ultimo):
                if nodo not in parziale:
                    parziale.append(nodo)
                    self.ricorsione(parziale, n_art)
                    print("Ricorsione avviata")
                    parziale.pop()


    def _get_score(self, parziale):
        score = 0
        for i in range(len(parziale) - 1):
            # Recupero il peso dell'arco tra il nodo i e il nodo i+1
            score += self.G[parziale[i]][parziale[i + 1]]["weight"]
        return score