import socket
import sys
from collections import OrderedDict
from pickle import loads
from random import randint
from threading import Thread
from time import time

import config


class Server:
    __sock = "socket.socket()"
    __quantity_users = 0
    __pairs_port = OrderedDict()
    __is_ready_field = {}
    __still_waiting = {}

    def __init__(self):
        self.__sock = socket.socket()
        self.__sock.bind((config.HOST, config.PORT))
        self.__sock.listen()
        self.__endless_loop()

    def __endless_loop(self):
        while True:
            client1, address = self.__sock.accept()
            print('connected:', address)
            self.__quantity_users += 1
            self.__still_waiting[client1] = "waiting"
            if self.__quantity_users % 2 == 0:
                client2, _ = self.__pairs_port.popitem()
                self.__pairs_port[client2] = client1
                self.__pairs_port[client1] = client2
                is_first = bool(randint(0, 1))
                self.__is_ready_field[client1] = False
                self.__is_ready_field[client2] = False
                t = Thread(target=self.__recv_state_waiting, args=(client1,))
                t.start()
                thread1 = Thread(target=self.__run, args=(client1, is_first))
                thread2 = Thread(target=self.__run, args=(client2, not is_first))
                thread1.start()
                thread2.start()
            else:
                self.__pairs_port[client1] = 0
                thread = Thread(target=self.__waiting_opponent, args=(client1,))
                thread.start()

    def __waiting_opponent(self, conn):
        number = self.__quantity_users
        t = Thread(target=self.__recv_state_waiting, args=(conn,))
        t.start()
        while number == self.__quantity_users and self.__still_waiting[conn] != "connect":
            if self.__still_waiting[conn] == "disconnect":
                print("disconnected:", conn.getpeername())
                self.__pairs_port.popitem()
                self.__quantity_users -= 1
                break

    def __recv_state_waiting(self, conn):
        conn.settimeout(1)
        start_time = time()
        data = bytes("", encoding="UTF-8")
        while not data.decode("UTF-8"):
            if time() - start_time >= config.TIME_WAITING_OPPONENT + 1:
                self.__still_waiting[conn] = "disconnect"
                return
            try:
                data = conn.recv(config.MEMORY_LIMIT_STR)
            except TimeoutError:
                pass
        self.__still_waiting[conn] = data.decode("UTF-8")

    @staticmethod
    def __recv_str(conn):
        conn.settimeout(1)
        time_wait = 1
        start_time = time()
        try:
            data = b""
            while not data and time() - start_time <= time_wait:
                data = conn.recv(config.MEMORY_LIMIT_STR)
        except TimeoutError:
            return 0
        except ConnectionResetError:
            return 0
        return data.decode("UTF-8")

    @staticmethod
    def __recv_tuple(conn):
        time_wait = config.TIME_WAITING_MOVE
        start_time = time()
        conn.settimeout(time_wait)
        try:
            data = 0
            while not data and time() - start_time <= time_wait:
                data = conn.recv(config.MEMORY_LIMIT_TUPLE)
        except TimeoutError:
            return 0
        except ConnectionResetError:
            return 0
        return tuple(data)

    def __request(self, conn, data):
        conn.send(bytes(data))
        return self.__recv_str(conn)

    @staticmethod
    def __recv_field(conn):
        time_wait = config.TIME_WAITING_CONSTRUCTOR_FIELD + config.TIME_WAITING_LOADING_WINDOW
        conn.settimeout(time_wait)
        try:
            data = 0
            while not data:
                data = conn.recv(config.MEMORY_LIMIT_FIELD)
            return data
        except TimeoutError:
            return 0
        except ValueError:
            return 0
        except EOFError:
            return 0
        except ConnectionResetError:
            return 0

    def __run(self, client, is_first):
        number_player = 2 - is_first
        client.send(bytes(number_player))
        while self.__still_waiting[client] == "waiting":
            pass
        data = self.__recv_field(client)
        self.__is_ready_field[client] = True
        try:
            while not self.__is_ready_field[self.__pairs_port[client]]:
                pass
            self.__pairs_port[client].send(data)
            if loads(data):
                print(sys.getsizeof(data))
            else:
                # print("ROUND")
                self.__remove_client(client)
                return
            if is_first:
                is_my_turn = is_first
                while True:
                    if is_my_turn:
                        data = self.__recv_tuple(client)
                        req = self.__request(self.__pairs_port[client], data)
                    else:
                        data = self.__recv_tuple(self.__pairs_port[client])
                        req = self.__request(client, data)
                    if not req:
                        self.__remove_client(client)
                        # print("ROUND")
                        break
                    elif req == "same":
                        is_my_turn = is_my_turn
                    elif req == "other":
                        is_my_turn = not is_my_turn
        except KeyError:
            pass
        except TimeoutError:
            try:
                self.__remove_client(self.__pairs_port[client])
            except KeyError:
                pass
            try:
                self.__remove_client(client)
            except KeyError:
                pass

    def __remove_client(self, client):
        if client in self.__is_ready_field.keys():
            self.__is_ready_field.pop(client)
        if client in self.__pairs_port.keys():
            self.__pairs_port.pop(client)


Server()
