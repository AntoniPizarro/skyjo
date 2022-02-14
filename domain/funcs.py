from random import randint
from typing import List

def shuffle(to_shuffle: List):
    '''
    Desordena de manera aleatoria una lista
    '''
    res = []
    length = len(to_shuffle)
    while len(res) != length:
        item = to_shuffle[randint(0, len(to_shuffle) - 1)]
        res.append(item)
        to_shuffle.remove(item)
    
    return res

if __name__ == "__main__":
    to_shuffle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(to_shuffle)
    print(shuffle(to_shuffle))
    print(to_shuffle)