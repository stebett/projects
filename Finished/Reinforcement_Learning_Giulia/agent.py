import random as rd
import numpy as np

# Questo file crea la classe Agent, con diverse funzioni
# che ti spieghero' mano a mano.
# In sintesi quello che fa e' costruire una griglia di valori,
# della stessa grandezza della griglia in cui si muove,
# e computa ogni valore in base al reward che ottiene spostandocisi
# sommato alla media dei valori circostanti:
# Per esempio, se l'agenta arriva in un punto con valore 0,
# e tutti i valori circostanti sono 0, e il reward che ottiene e' -1,
# l'operazione che fara' sara' -1 + 0*4 = -1
# In questo modo l'agente crea una tabella con valori tanto inferiori
# quanto sono lontani dal punto di arrivo
# Questo agente e' basato su un algoritmo con diverse caratteristiche:
# 1) q_learning -> Non attribuisce valori agli stati ma alle azioni
# 2) TD(0) -> Temporal Difference 0, ovvero ogni mossa rielabora i valori delle
# azioni
# 3) off-policy -> Agisce sempre nel modo piu' conveniente (greedy)


class Agent:
    def __init__(self, grid_shape, target, discount):
        self.max_lenght = grid_shape - 1  # Numpy parte a contare da 0
        # Ora inizializzo la griglia di valori.
        # Si chiamano q_values per qualche motivo che non ricordo
        self.q_values = np.zeros([grid_shape, grid_shape])
        # Definisco il target adattandolo a numpy
        self.target = (target[0] - 1, target[1] - 1)
        # Questo e' un numero che serve a diminuire il
        # valore percepito di reward futuri,
        # ovvero quanto l'agente deve preferire
        # un reward immediato ad uno futuro.
        self.gamma = discount
        # Inizializzo la posizione di partenza a 0
        self.pos = None

    def get_real_pos(self, position):
        # Prende come input lo stato e lo salva adattandolo a numpy
        real_position = (position[0] - 1, position[1] - 1)
        self.pos = real_position

    def look_around(self):
        # Legge i valori attesi di ogni cella adiacente
        # L'if statement serve ad evitare un index error:
        # se la cella attuale e' al margine, il valore che avra':
        # come input sara' se stessa,
        # anziche' quella che uscirebbe dal margine
        top_pos = ((self.pos[0] - 1, self.pos[1])
                   if self.pos[0] - 1 >= 0
                   else (self.pos[0], self.pos[1]))
        bot_pos = ((self.pos[0] + 1, self.pos[1])
                   if self.pos[0] + 1 <= self.max_lenght
                   else (self.pos[0], self.pos[1]))
        left_pos = ((self.pos[0], self.pos[1] - 1)
                    if self.pos[1] - 1 >= 0
                    else (self.pos[0], self.pos[1]))
        right_pos = ((self.pos[0], self.pos[1] + 1)
                     if self.pos[1] + 1 <= self.max_lenght
                     else (self.pos[0], self.pos[1]))
        # Creo una tupla di tuple
        # (devono essere hashabili per usarle come chiavi per
        # il dizionario), con valori le coordinate della posizione
        # e la stringa per rappresentarla
        neighbours = ((bot_pos, 'bot'),
                      (top_pos, 'top'),
                      (left_pos, 'left'),
                      (right_pos, 'right'))
        # Creo un dizionario con valori i q_values delle
        # celle adiacenti e come chiavi le stringhe per rappresentarle
        move_dict = {neighbours[pos][1]: self.q_values[neighbours[pos][0]]
                     for pos in range(4)}
        # Do come output il dizionario
        return move_dict

    def choose_move(self):
        # Salvo l'output di look_around
        move_values = self.look_around()

        # Salvo il q-valore massimo delle celle adiacenti
        max_value = max(move_values.values())

        # Itero in un ciclo per trovare tutte le mosse ch
        # e porterebbero a celle con uguali q-valori
        top_moves = []
        for key, value in move_values.items():
            if value == max_value:
                top_moves.append(key)
        # Come output mando una a caso tra quelle mosse,
        # se ce n'e' una sola scegliera' quella per forza.
        return rd.choice(top_moves)

    def take_reward(self):
        # Controllo di non essere arrivato alla fine,
        # e do un reward di conseguenza.
        # I valori dei reward sono arbitrari, l'importante e' che
        # quello del target sia maggiore del resto.
        # Il q-valore della cella target per questo tipo
        # di problema e' sempre 0
        if self.pos == self.target:
            return 0
        else:
            return -1

    def evaluate_q_value(self):
        # Prendo il reward
        reward = self.take_reward()
        # Se e' 0 capisco che ho vinto e esco.
        if reward == 0:
            self.q_values[self.pos] = 0
            return 'finish'
        # Altrimenti prendo i valori che ho attorno
        move_values = self.look_around()
        # Faccio la media tra di loro, la moltiplico per
        # il discount, o gamma, e la sommo al reward
        new_q_value = 0.25*sum(move_values.values()) * \
            self.gamma + reward
        # Poi assegno questo valore alla cella su coi mi trovo
        self.q_values[self.pos] = new_q_value
