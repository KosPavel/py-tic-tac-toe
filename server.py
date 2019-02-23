from socket import *
import socket
import random
import pickle

mainfield = ['u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', '']

sock = socket.socket(AF_INET, SOCK_STREAM)
host = ''
port = 8000
print('ready on ' + str(socket.gethostbyname(socket.gethostname())) + ':' + str(port));
sock.bind((host, port))
sock.listen(2)

conn1, addr1 = sock.accept()
symbol1 = str(random.randint(1, 2))
conn1.send(symbol1.encode("utf-8"))
print('player 1 connected, conn1 = ' + str(conn1))

conn2, addr2 = sock.accept()
if symbol1 == '1':
    symbol2 = '2'
    player_turn = 1 #первым ходит игрок Х
else:
    symbol2 = '1'
    player_turn = 2 #первым ходит игрок Х
conn2.send(symbol2.encode("utf-8"))
print('player 2 connected, conn1 = ' + str(conn2))

#соединение установлено, далее игра
def checkwin():
    if mainfield[0] == mainfield[1] == mainfield[2] == symbol1:
        answer = 'player 1 won'
    elif mainfield[3] == mainfield[4] == mainfield[5] == symbol1:
        answer = 'player 1 won'
    elif mainfield[6] == mainfield[7] == mainfield[8] == symbol1:
        answer = 'player 1 won'
    elif mainfield[0] == mainfield[3] == mainfield[6] == symbol1:
        answer = 'player 1 won'
    elif mainfield[1] == mainfield[4] == mainfield[7] == symbol1:
        answer = 'player 1 won'
    elif mainfield[2] == mainfield[5] == mainfield[8] == symbol1:
        answer = 'player 1 won'
    elif mainfield[0] == mainfield[4] == mainfield[8] == symbol1:
        answer = 'player 1 won'
    elif mainfield[6] == mainfield[4] == mainfield[2] == symbol1:
        answer = 'player 1 won'
    elif mainfield[0] == mainfield[1] == mainfield[2] == symbol2:
        answer = 'player 2 won'
    elif mainfield[3] == mainfield[4] == mainfield[5] == symbol2:
        answer = 'player 2 won'
    elif mainfield[6] == mainfield[7] == mainfield[8] == symbol2:
        answer = 'player 2 won'
    elif mainfield[0] == mainfield[3] == mainfield[6] == symbol2:
        answer = 'player 2 won'
    elif mainfield[1] == mainfield[4] == mainfield[7] == symbol2:
        answer = 'player 2 won'
    elif mainfield[2] == mainfield[5] == mainfield[8] == symbol2:
        answer = 'player 2 won'
    elif mainfield[0] == mainfield[4] == mainfield[8] == symbol2:
        answer = 'player 2 won'
    elif mainfield[6] == mainfield[4] == mainfield[2] == symbol2:
        answer = 'player 2 won'
    else:
        filled = 0
        for i in range(9):
            if mainfield[i] != 'u':
                filled += 1
        if filled == 9:
            answer = 'draw'
        else:
            answer = 'continue'
    print('answer = ' + answer)
    return answer

def makeTurn():
    global player_turn
    global conn1
    global conn2
    # получение хода от игрока
    if player_turn == 1:
        pickleddata = conn1.recv(1024)
        data = pickle.loads(pickleddata)

        for i in range(9):
            mainfield[i] = data[i]

        answer = checkwin()

        if answer == 'player 1 won':
            if symbol1 == '1':
                mainfield[9] = 'X'
            elif symbol1 == '2':
                mainfield[9] = 'O'
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)
            conn2.send(pickleddata)
            conn1.close()
            conn2.close()
        elif answer == 'player 2 won':
            if symbol2 == '1':
                mainfield[9] = 'X'
            elif symbol2 == '2':
                mainfield[9] = 'O'
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)
            conn2.send(pickleddata)
            conn1.close()
            conn2.close()
        elif answer == 'draw':
            mainfield[9] = 'd'
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)
            conn2.send(pickleddata)
            conn1.close()
            conn2.close()
        else:
            pickleddata = pickle.dumps(mainfield)
            conn2.send(pickleddata)

        player_turn = 2
    else:
        pickleddata = conn2.recv(1024)
        data = pickle.loads(pickleddata)

        for i in range(9):
            mainfield[i] = data[i]
        
        answer = checkwin()

        if answer == 'player 1 won':
            if symbol1 == '1':
                mainfield[9] = 'X'
            elif symbol1 == '2':
                mainfield[9] = 'O'
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)
            conn2.send(pickleddata)
            conn1.close()
            conn2.close()
        elif answer == 'player 2 won':
            if symbol2 == '1':
                mainfield[9] = 'X'
            elif symbol2 == '2':
                mainfield[9] = 'O'
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)
            conn2.send(pickleddata)
            conn1.close()
            conn2.close()
        elif answer == 'draw':
            mainfield[9] = 'd'
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)
            conn2.send(pickleddata)
            conn1.close()
            conn2.close()
        else:
            pickleddata = pickle.dumps(mainfield)
            conn1.send(pickleddata)

        player_turn = 1


z = 0
while z == 0:
    makeTurn()