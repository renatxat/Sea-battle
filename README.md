# Morskoy-boy
Проект:
    Реализация игры "Морской Бой" на python. Автор: Хатымов Ренат, Б05-224.
По поводу багов и ошибок писать на: t.me/renatxat

Установка:
На данный момент онлайн-сервер отключён, поэтому light способ не работает.
Также вы не можете играть с разных устройств.

Light:
Pyinstaller.
- Если у вас windows, запустите файл sea-battle.exe из папки /game/windows
- Eсли у вас linux, зайдите в консоли в папку /game/linux и пропишите:
sudo chmod +x sea-battle && ./sea-battle
- Если у вас macos, то воспользуйтесь одним из других способов. 

Medium:
Bash script.
coming soon...

Hard:
Ручками.
0) Установите python 3.10+ (иначе у вас могут вылетать ошибки в консоль)
1) Запустите файл server.py при помощи команды:
python3.10 server.py
2) Поменяйте значение параметра HOST в файле config.py на 'localhost',
если хотите запустить сервер локально (удалённый может не работать)
3) Пропишите в терминале:
pip install -r requirements.txt
Если у вас linux, то скачайте ещё модуль tkinter при помощи следующих команд:
sudo apt update
sudo apt install python3-tk
4) Запустите файл main.py при помощи команды:
python3.10 main.py