import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.n_min_album = 0

    def handle_create_graph(self, e):
        self._model.build_graph(self.n_min_album)

        n_nodi, n_archi = self._model.get_g_details()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.btnSearchArtists.disabled = False

        self.populate_dd_artist()


        self._view.update_page()

    def handle_connected_artists(self, e):
        artista_scelto = int(self._view.ddArtist.value)

        lista_vicino_peso = self._model.get_neighbors(artista_scelto)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista scelto: {len(lista_vicino_peso)}"))
        for v, peso in lista_vicino_peso:
            self._view.txt_result.controls.append(ft.Text(f"{v} - Numero di generi in comune: {peso}"))

        self._view.update_page()

    def check_n_album(self, e):
        self.n_min_album = int(self._view.txtNumAlbumMin.value)

        if self.n_min_album <= 0:
            self.n_min_album = None
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Errore: inserire un numero maggiore di zero."))
            self._view.update_page()
        else:
            print("Valore salvato con successo.")


    def populate_dd_artist(self):
        nodi = self._model.nodi

        for n in nodi:
            self._view.ddArtist.options.append(ft.dropdown.Option(key = str(n.id), text = n.name))

        self._view.update_page()


    def check_values_durata(self, e):
        min_durata = float(self._view.txtMinDuration.value)

        if min_durata <= 0:
            min_durata = None
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Errore: Inserire una durata maggiore di zero."))

        self._view.update_page()

        print("Durata salvata con successo")


    def check_values_artists(self, e):
        max_artists = int(self._view.txtMaxArtists.value)

        if max_artists < 1 or max_artists > len(self._model.nodi):
            max_artists = None
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Errore: Inserire un numero compreso tra 1 e {len(self._model.nodi)}."))

        self._view.update_page()

        print("Numero artisti salvato con successo")

    def handle_recursion(self, e):
        artista_scelto = int(self._view.ddArtist.value)
        n_art = int(self._view.txtMaxArtists.value)
        d_min = float(self._view.txtMinDuration.value)


        path, total_weight = self._model.get_best_path(artista_scelto, n_art, d_min)

        self._view.txt_result.controls.clear()

        for i in range(len(path)):
            nodo = path[i]
            # Se è il primo nodo non mettiamo la freccia
            if i == 0:
                self._view.txt_result.controls.append(ft.Text(f"{nodo.Name}"))
            else:
                # Stampiamo anche il peso dell'arco tra il precedente e l'attuale (opzionale)
                peso_arco = self._model.G[path[i - 1]][path[i]]['weight']
                self._view.txt_result.controls.append(ft.Text(f" -> (peso: {peso_arco}) -> {nodo.Name}"))

        self._view.update_page()