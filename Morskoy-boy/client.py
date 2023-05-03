import socket
import tkinter as tk
from _tkinter import TclError
from math import ceil
from pickle import dumps, loads
from sys import platform
from threading import Thread
from time import time
from tkinter import messagebox

import config
from battlefield_opponent_view import BattlefieldOpponent
from battlefield_player_view import BattlefieldPlayer
from constructor_fields import ConstructorFields
from window import Window


class Client:
    __window = ["Window()"]
    __canvas = ["tk.Canvas()"]

    __field = ["BattlefieldPlayer"]
    __foreign_field = ["BattlefieldOpponent"]
    __data_field = "waiting"

    __label_turn = ["tk.Label()"]
    __label_wait = ["tk.Label()"]
    __is_closing = False
    __editing = "disconnection"

    __timer = config.TIME_WAITING_MOVE
    __start_time_move = "time()"
    __text_before_timer = str
    __I_was_waiting_opponent = True
    __sock = ["socket.socket()"]
    __is_my_first_move = "waiting"

    def __init__(self):
        self.__sock = socket.socket()
        self.__sock.connect((config.HOST, config.PORT))
        mem_lim = 128
        t = Thread(target=self.__get_is_my_first_move, args=(mem_lim,))
        t.start()
        self.__create_waiting_room()
        self.__create_boards()
        self.__draw_boards()
        self.__start_loops()

    def __get_is_my_first_move(self, mem_lim):
        try:
            self.__sock.settimeout(config.TIME_WAITING_OPPONENT + 1)
            data = self.__sock.recv(mem_lim)
            self.__is_my_first_move = len(list(data)) == 1
            self.__sock.send(bytes("recd", encoding="UTF-8"))
        except TimeoutError:
            self.__is_closing = True
            self.__is_my_first_move = "error"
        except OSError:
            self.__is_closing = True
            self.__is_my_first_move = "error"

    def __create_waiting_room(self):
        window = Window(is_game_field=False)
        label_wait = tk.Label(window,
                              relief="solid",
                              font=("Comic Sans MS", 13, "bold"),
                              text="""У вас будет 60 секунд, чтобы расставить корабли.
На каждый ход даётся 15 секунд. Удачной игры!\nИщем соперника...\n |""",
                              justify="center",
                              borderwidth=1)
        label_wait.pack()
        start_time = time()
        boot_symbols = "|/–\\"
        number_symbols = 0
        time_update_symbol = time()
        while self.__is_my_first_move == "waiting" or time() - start_time < config.TIME_WAITING_LOADING_WINDOW:
            if self.__is_my_first_move != "waiting":
                self.__I_was_waiting_opponent = False
            if window.is_destroyed() or self.__is_closing:
                self.__sock.send(bytes("disconnect", encoding="UTF-8"))
                self.__is_closing = True
                break
            if time() - time_update_symbol > 0.4:
                time_update_symbol = time()
                number_symbols = (number_symbols + 1) % len(boot_symbols)
                label_wait["text"] = label_wait["text"][:-1] + boot_symbols[number_symbols]
                window.update()
        window.destroy()
        if self.__is_my_first_move == "error":
            messagebox.showinfo(title="Ошибка 408", message="Время ожидания истекло...")

    def __create_boards(self):
        if self.__is_closing:
            self.__sock.close()
            return
        start_time = time() + 1
        # 1 second for drawing constructor_field
        constructor_field = ConstructorFields(presence_timer=True)
        print(6)
        constructor_field = constructor_field.get()
        self.__sock.send(dumps(constructor_field))
        print(7)
        if not constructor_field:
            print(8)
            self.__sock.close()
            self.__is_closing = True
            return
        time_wait = ceil(config.TIME_WAITING_CONSTRUCTOR_FIELD + start_time - time() +
                         config.TIME_WAITING_LOADING_WINDOW * self.__I_was_waiting_opponent)
        # opponent could start config.TIME_WAITING_LOADING_WINDOW seconds later, because he located in window waiting
        print(9)
        self.__update_timer_waiting_field(time_wait)
        print(10)
        if not self.__data_field and not self.__window.is_destroyed():
            self.__is_closing = True
            self.__show_window_game_over("Мог, но не стал", "Ваш противник сдался :(")
            return
        self.__window.destroy()
        self.__window = Window(is_game_field=True)
        if platform.startswith('win'):
            resizing_constant = 4
        else:
            resizing_constant = 2
        self.__canvas = tk.Canvas(self.__window,
                                  width=(config.COLUMN * 2 + 1) * config.SIZE_OF_CELL - resizing_constant,
                                  height=(config.ROW + 1) * config.SIZE_OF_CELL - resizing_constant)
        # the order in which the fields are created is very important
        # it has to do with filling the canvas with buttons
        self.__foreign_field = BattlefieldOpponent(self.__data_field, self.__canvas)
        self.__field = BattlefieldPlayer(constructor_field + [], self.__canvas)

    def __update_timer_waiting_field(self, time_wait):
        self.__window = Window(is_game_field=False)
        self.__label_wait = tk.Label(self.__window,
                                     relief="solid",
                                     font=("Comic Sans MS", 13, "bold"),
                                     text="Ожидаем соперника...",
                                     justify="center",
                                     borderwidth=1)
        self.__label_wait.pack()
        start_time = time() - 1
        text = self.__label_wait["text"]
        t = Thread(target=self.__recv_field, args=(time_wait,))
        t.start()
        while time_wait >= 0 and not self.__is_closing and self.__data_field == "waiting" \
                and not self.__window.is_destroyed():
            if time() - start_time >= 1:
                start_time = time()
                self.__label_wait["text"] = text + f"({str(time_wait)})"
                time_wait -= 1
                self.__window.update()
        if self.__data_field == "waiting":
            self.__data_field = []
        if self.__window.is_destroyed():
            self.__is_closing = True
        else:
            self.__label_wait["text"] = text + "(0)"

    def __recv_field(self, time_wait):
        try:
            self.__sock.settimeout(time_wait)
            mem_lim = 2048
            print(0)
            data = self.__sock.recv(mem_lim)
            print(1)
            self.__data_field = loads(data)
            print(2)
        except TimeoutError:
            self.__data_field = []
        except OSError:
            self.__data_field = []
        except ValueError:
            self.__data_field = []
        except EOFError:
            self.__data_field = []

    def __draw_boards(self):
        if self.__is_closing:
            self.__sock.close()
            return
        self.__field.view()
        self.__foreign_field.view()
        self.__create_label_turn()
        self.__canvas.pack()
        self.__window.resizable(width=False, height=False)
        self.__start_time_move = time()

    def __create_label_turn(self):
        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.COLUMN + 1) * config.SIZE_OF_CELL - 2 * (
                                       (2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3),
                               height=config.SIZE_OF_CELL,
                               bg="white")
        label_frame.pack_propagate(False)
        self.__label_turn = tk.Label(label_frame,
                                     relief="solid",
                                     font=("Comic Sans MS", 13, "bold"),
                                     justify="center",
                                     borderwidth=1)
        if self.__is_my_first_move:
            self.__timer = config.TIME_WAITING_MOVE + 1
            self.__text_before_timer = "Ваш ход"
            self.__label_turn.configure(text=self.__text_before_timer + f"({self.__timer})", fg="lime")
            self.__foreign_field.let_me_move()
        else:
            self.__timer = config.TIME_WAITING_MOVE + 2
            # player waits more than moves, because his timer started early
            self.__text_before_timer = "Ход противника"
            self.__label_turn.configure(text=self.__text_before_timer + f"({self.__timer})", fg="red")
            self.__foreign_field.existence_hit_last_shot()
        self.__label_turn.pack(fill="both", expand=True)
        self.__canvas.create_window(((2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3,
                                     config.ROW * config.SIZE_OF_CELL),
                                    anchor="nw",
                                    window=label_frame)

    def __start_loops(self):
        if self.__is_closing:
            self.__sock.close()
            return
        self.__window.after_idle(self.__loop, 0)  # start endless __loop
        self.__window.mainloop()

    def __loop(self, n):
        if self.__is_closing or type(self.__window) == str or self.__window.is_destroyed():
            self.__sock.close()
            return
        if n == 0:
            self.__window.after(1, self.__loop, n + 1)
        self.__click_processing()
        self.__check_game_over(n)

    def __click_processing(self):
        if self.__foreign_field.presence_of_changes() and self.__label_turn["fg"] == "lime":
            self.__sock.send(bytes(self.__foreign_field.get_last_shot()))
            if not self.__foreign_field.existence_hit_last_shot():
                self.__text_before_timer = "Ход противника"
                self.__create_timer("red")
                self.__editing = "disconnection"
            else:
                self.__create_timer("lime")
        elif self.__editing == "disconnection" and self.__label_turn["fg"] == "red":
            self.__editing = "waiting"
            t = Thread(target=self.__recv_tuple, args=())
            t.start()
        elif self.__editing != "waiting" and self.__editing != "disconnection" and self.__label_turn["fg"] == "red":
            if not self.__editing and not self.__window.is_destroyed():
                self.__label_turn["text"] = self.__text_before_timer + "(0)"
                self.__show_window_game_over("~Вы выиграли!", "Потеряно соединение с соперником.")
                return
            self.__field.update(*self.__editing)
            self.__editing = "disconnection"
            if self.__field.existence_hit_last_shot():
                self.__sock.send(bytes("same", encoding="UTF-8"))  # move same player
                self.__create_timer("red")
            else:
                self.__sock.send(bytes("other", encoding="UTF-8"))  # move other player
                self.__foreign_field.let_me_move()
                self.__foreign_field.existence_hit_last_shot()
                self.__text_before_timer = "Ваш ход"
                self.__create_timer("lime")
        else:
            self.__update_timer()

    def __recv_tuple(self):
        time_wait = config.TIME_WAITING_MOVE + 1
        try:
            self.__sock.settimeout(time_wait)
            mem_lim = 256
            data = self.__sock.recv(mem_lim)
            self.__editing = tuple(data)
        except TimeoutError:
            self.__editing = 0
        except OSError:
            self.__editing = 0
        except ValueError:
            self.__data_field = 0

    def __create_timer(self, color):
        self.__start_time_move = time()
        self.__timer = config.TIME_WAITING_MOVE + 1 + (color == "red")
        self.__label_turn.configure(text=self.__text_before_timer + f"({str(self.__timer)})", fg=color)

    def __update_timer(self):
        if time() - self.__start_time_move >= config.TIME_WAITING_MOVE - self.__timer + 1:
            self.__timer = max(config.TIME_WAITING_MOVE - int(time() - self.__start_time_move), 0)
            self.__label_turn["text"] = self.__text_before_timer + f"({str(self.__timer)})"
        if self.__timer == 0 and self.__label_turn["fg"] == "lime":
            self.__show_window_game_over("Вы проиграли :(", "Время истекло")

    def __check_game_over(self, n):
        if self.__foreign_field.get_run() and self.__field.get_run():
            self.__window.after(1, self.__loop, n + 1)  # endless cycle!
        elif self.__field.get_run():
            self.__show_window_game_over("Чел, хорош!", "Вы победили!")
        else:
            self.__show_window_game_over("Лох", "Вы проиграли :(")

    def __show_window_game_over(self, ttl, msg):
        try:
            self.__sock.close()
            self.__window.grab_set()
            if ttl == "Чел, хорош!" or ttl == "Лох":
                if messagebox.showinfo(title=ttl,
                                       message=msg,
                                       parent=self.__window):
                    self.__window.destroy()
            else:
                if messagebox.showwarning(title=ttl,
                                          message=msg,
                                          parent=self.__window):
                    self.__window.destroy()
        except TclError:
            pass
