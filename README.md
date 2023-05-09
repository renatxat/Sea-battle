# Morskoy-boy
Проект:
    Реализация игры "Морской Бой" на python. Автор: Хатымов Ренат, Б05-224.
По поводу багов и ошибок писать на: t.me/renatxat

Установка:

Light:
1) Pyinstaller.
Запустите файл sea-battle.exe из папки /game/windows, если у вас windows.
Зайдите в коносли в папку /game/linux и пропишите:
sudo chmod +x sea-battle && ./sea-battle
если у вас linux.
Воспользуйтесь другим способом, если у вас macos. 

Medium:
1) Docker. Скачайте sea-battle.tar из корня проекта.
2) Распакуйте его при помощи docker load <sea-battle.tar
3) Запустите полученный образ:
docker run -i -t --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro --name="rdev" sea-battle

Hard:
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