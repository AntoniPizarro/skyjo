from domain.funcs import *

class Card:

    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

class Player:

    def __init__(self, name, password, votation=False):
        self.maze = []
        self.revealed_cards = []
        self.hand = None
        self.name = name
        self.password = password
        self.votation = votation
        for i in range(12):
            self.revealed_cards.append(False)

    def get_maze(self):
        return self.maze

    def set_maze(self, maze):
        self.maze = maze
    
    def get_revealed(self):
        return self.revealed_cards
    
    def to_reveal(self, position):
        self.revealed_cards[position] = True

    def discard(self, deck):
        deck.discard_card(self.hand)
        self.hand = None
        for i in range(4):
            self.discard_line(i, deck)

    def get_name(self):
        return self.name
        
    def get_password(self):
        return self.password
    
    def get_vote(self):
        return self.votation

    def vote(self):
        if not self.votation:
            self.votation = True

    def take_card(self, card):
        self.hand = card

    def lines(self):
        '''
        Devuelve una lista con las columnas que se pueden descartar
        '''
        res = []
        for i in range(4):
            if self.get_maze()[i].get_value() == self.get_maze()[i + 4].get_value() and self.get_maze()[i].get_value() == self.get_maze()[i + 8].get_value():
                res.append(i)
        return res
    
    def discard_line(self, line, deck):
        '''
        Si la columna indicada esta compuesta por los mismos valores en las 3 cartas, se descartan las cartas
        '''
        if self.get_maze()[line].get_value() == self.get_maze()[line + 4].get_value() and self.get_maze()[line].get_value() == self.get_maze()[line + 8].get_value():
            card_0 = self.get_maze()[line]
            card_4 = self.get_maze()[line + 4]
            card_8 = self.get_maze()[line + 8]

            self.maze[line] = None
            self.maze[line + 4] = None
            self.maze[line + 8] = None

            self.revealed_cards[line] = True
            self.revealed_cards[line + 4] = True
            self.revealed_cards[line + 8] = True

            deck.discard_card(card_0)
            deck.discard_card(card_4)
            deck.discard_card(card_8)

    def change_card(self, maze_card, deck):
        '''
        Se le indica la posición de la carta del mazo que se quiere cambiar
        y la intercambia por la que hay en la mano. La carta cambiada se descarta
        '''
        to_change = self.maze[maze_card]
        self.maze[maze_card] = self.hand
        self.revealed_cards[maze_card] = True
        deck.discard_card(to_change)
        self.hand = None

    def get_data(self):
        return {"name" : self.get_name(), "password" : self.get_password(), "vote" : self.get_vote()}

class Deck:

    def __init__(self):
        self.deck = []
        self.discarted = []
        cards = {
            -2 : 10,
            -1 : 10,
            0 : 10,
            1 : 10,
            2 : 10,
            3 : 10,
            4 : 10,
            5 : 10,
            6 : 10,
            7 : 10,
            8 : 10,
            9 : 10,
            10 : 10,
            11 : 10,
            12 : 10
        }
        for value in cards:
            for i in range(cards[value]):
                self.deck.append(Card(value))

        self.shuffle_deck()
    
    def get_deck(self):
        '''
        Obtiene la baraja
        '''
        return self.deck
    
    def discard_card(self, card):
        '''
        Añade una carta de la baraja al montón de descarte
        '''
        self.discarted.append(card)
    
    def last_discarted(self):
        if self.discarted:
            return self.discarted[-1]
        
        return None

    def shuffle_deck(self):
        '''
        Baraja las cartas de forma aleatoria
        '''
        self.deck = shuffle(self.deck)
    
    def first_card(self):
        '''
        Devuelve la carta de arriba de la baraja
        '''
        card = self.deck[0]
        self.deck = self.deck[1:]

        return card

    def distribute(self, players):
        '''
        Reparte cartas a los jugadores de una lista
        '''
        for player in players:
            player.set_maze(self.deck[:12])
            self.deck = self.deck[12:]
        
        self.discard_card(self.deck[0])
        self.deck.pop(0)

class Game:

    def __init__(self, deck: Deck, players: List = []):
        self.deck = deck
        self.players = players
        if self.players:
            self.next_turn = self.get_players()[0]
        self.started = False
    
    def get_next_turn(self):
        return self.next_turn

    def start_game(self):
        if not self.started and self.votes() >= 2:
            self.started = True

    def game_status(self):
        return self.started

    def get_deck(self):
        return self.deck
    
    def get_players(self):
        return self.players
    
    def get_player(self, player_query):
        for player in self.get_players():
            if player.get_name() == player_query.get_name() and player.get_password() == player_query.get_password():
                return player
        
        return False

    def votes(self):
        votes = 0
        for player in self.get_players():
            if player.get_vote():
                votes += 1
        
        return votes

    def add_player(self, new_player):
        if len(self.get_players()) >= 12:
            return False
        
        for player in self.get_players():
            if player.get_name() == new_player.get_name():
                return False

        self.players.append(new_player)
        self.next_turn = self.get_players()[0]
        return new_player
    
    def total_scores(self):
        res = {}
        for player in self.get_players():
            score = 0
            for card in player.get_maze():
                if card:
                    score += card.get_value()
            res[player.get_name()] = score
        
        return res