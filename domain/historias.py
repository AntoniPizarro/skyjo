from classes import *
from random import randint

def revelar_cartas(player):
    res = ""
    count = 0
    for card in player.get_maze():
        count += 1
        index = player.get_maze().index(card)
        if player.get_revealed()[index] == True:
            if card:
                res += f"{card.get_value()} "
            else:
                res += f"{None} "
        else:
            res += "# "
        if count >= 4:
            res += "\n"
            count = 0
            
    if res[-1] == "\n":
        res = res[:-1]

    return res

def print_maze(player: Player):
    maze = player.get_maze()
    print(f"\nJugador {player.get_name()}:")
    print(f"{maze[0].get_value()} {maze[1].get_value()} {maze[2].get_value()} {maze[3].get_value()}")
    print(f"{maze[4].get_value()} {maze[5].get_value()} {maze[6].get_value()} {maze[7].get_value()}")
    print(f"{maze[8].get_value()} {maze[9].get_value()} {maze[10].get_value()} {maze[11].get_value()}")

# Se genera un mazo
deck = Deck()



# Se generan los jugadores
player_1 = Player("Toni", "123")
player_2 = Player("Damián", "123")
player_3 = Player("Adrián", "123")

print(f"Jugador {player_1.get_name()} generado")
print(f"Jugador {player_2.get_name()} generado")
print(f"Jugador {player_3.get_name()} generado")

players = [player_1, player_2, player_3]



# Se genera una partida
game = Game( deck, players)



# Asignamos las cartas a cada jugador
deck.distribute(players)

print_maze(player_1)
print_maze(player_2)
print_maze(player_3)



# El jugador 1 revela dos de sus cartas
print(f"\nJugador {player_1.get_name()}: Revela 2 de sus cartas")
print(revelar_cartas(player_1))
player_1.to_reveal(0)
player_1.to_reveal(11)
print("\n")
print(revelar_cartas(player_1))



# El jugador 2 revela dos de sus cartas
print(f"\nJugador {player_2.get_name()}: Revela 2 de sus cartas")
print(revelar_cartas(player_2))
player_2.to_reveal(2)
player_2.to_reveal(9)
print("\n")
print(revelar_cartas(player_2))



# El jugador 3 revela dos de sus cartas
print(f"\nJugador {player_3.get_name()}: Revela 2 de sus cartas")
print(revelar_cartas(player_3))
player_3.to_reveal(4)
player_3.to_reveal(5)
print("\n")
print(revelar_cartas(player_3))



# El jugador 1 coge una carta de la baraja y la cambia por una de sus cartas
print(f"\nJugador {player_1.get_name()}: coge una carta de la baraja y la cambia")
print(revelar_cartas(player_1))
carta = deck.first_card()
player_1.take_card(carta)
player_1.change_card(1, deck)
print("\n")
print(revelar_cartas(player_1))



# El jugador 2 coge la carta descartada por el jugador 1 y la cambia por una de sus cartas
print(f"\nJugador {player_2.get_name()}: coge la carta descartada por el jugador 1 y la cambia")
print(revelar_cartas(player_2))
carta = deck.last_discarted()
player_2.take_card(carta)
player_2.change_card(5, deck)
print("\n")
print(revelar_cartas(player_2))



# El jugador 3 coge la carta de la baraja pero no le gusta y la descarta, revelando una de las suyas
print(f"\nJugador {player_3.get_name()}: coge la carta de la baraja pero no le gusta y la descarta")
print(revelar_cartas(player_3))
carta = deck.first_card()
player_3.take_card(carta)
player_3.discard(deck)
player_3.to_reveal(7)
print("\n")
print(revelar_cartas(player_3))



# Todos los jugadores revelan todas sus cartas
for i in range(len(player_1.get_maze())):
    player_1.to_reveal(i)
    
for i in range(len(player_2.get_maze())):
    player_2.to_reveal(i)
    
for i in range(len(player_3.get_maze())):
    player_3.to_reveal(i)


print(f"\nJugador {player_1.get_name()}: revela todas sus cartas")
print(revelar_cartas(player_1))

print(f"\nJugador {player_2.get_name()}: revela todas sus cartas")
print(revelar_cartas(player_2))

print(f"\nJugador {player_3.get_name()}: revela todas sus cartas")
print(revelar_cartas(player_3))



# El jugador 1 tiene unas cuantas filas pendientes de descarte
new_maze = [
    Card(-1), Card(2), Card(1), Card(4),
    Card(-1), Card(6), Card(1), Card(8),
    Card(-1), Card(10), Card(1), Card(12)
]
old_maze = player_1.get_maze()
player_1.set_maze(new_maze)
print(f"\nJugador {player_1.get_name()}: descarta columnas")
print(revelar_cartas(player_1))
lines = player_1.lines()
print(f"\n{lines}")
player_1.discard_line(lines[1], deck)
print("\n")
print(revelar_cartas(player_1))



# Se cuentan los puntos de todos los jugadores
print("\nPuntuaciones totales:")
print(game.total_scores())