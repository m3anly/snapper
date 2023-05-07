import paramiko
import sqlite3
import sys

# Создание базы данных и таблицы для хранения данных входа на сервер
conn = sqlite3.connect("DENIS_LOH.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS login_data (hostname TEXT, username TEXT, password TEXT)")
conn.commit()
print("  ======================================================================")
print("  корпорация хуйнясофт представляет: снапшотилка для есхи версия 0.1.хуй")
# Проверка наличия записи в базе данных и использование сохраненных данных при их наличии
cursor.execute("SELECT * FROM login_data")
row = cursor.fetchone()
if row is not None:
    hostname, username, password = row
else:
    # Запрос адреса сервера, логина и пароля
    print("  ======================================================================")
    print("  Забавный факт: Эти данные надо вводить лишь раз,")
    print("  дальше они будут храниться в базе в папке с прогой. ")
    print("  Это сообщение больше не выведется. Никогда...")
    print("  ofc if you'll not remove .db file in app's dir ")
    print("  ======================================================================")
    hostname = input("  айпи сервера: ")
    username = input("  юзер: ")
    password = input("  пороль: ")
    cursor.execute("INSERT INTO login_data VALUES (?, ?, ?)", (hostname, username, password))
    conn.commit()

# Подключение к серверу
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password)

# Получение списка виртуальных машин и их идентификаторов

print("  =====================")
print("  Вот твои тачки, босс:")
print("  =====================")
stdin, stdout, stderr = ssh.exec_command("vim-cmd vmsvc/getallvms")
output = stdout.read().decode("utf-8")
vm_list = output.strip().split("\n")[1:]
vm_dict = {}
for vm in vm_list:
    vm_info = vm.strip().split()
    vm_id = vm_info[0]
    vm_name = vm_info[1].strip('[]')
    vm_dict[vm_id] = vm_name
    print(f"  ID: {vm_id}\tИмя: {vm_name}")
    
# Выбор действия
print("  =====================")
choice = input("  Чё дальше? (1 - Создать снапшот, 2 - не доделалa, 3 - выйти в окно): ")
print("  =====================")

if choice == "1":
    # Создание снапшота
    print("  =====================")
    vm_id = input("  Сюда вводишь ID (оно слева ебать): ")
    print("  =====================")
    snapshot_name = input("  Сюда название снапшота (сам хоть не запутайся в них чурка): ")
    cmd = f"vim-cmd vmsvc/snapshot.create {vm_id} {snapshot_name}"
elif choice == "2":
    print("  =====================")
    print(f"  Не работает нихуя, сказалa же - не допилено")
    print("  =====================")
    sys.exit()
elif choice == "3":
    print("  =====================")
    print(f"  Я тебя запомню, ещё увидимся...")
    print("  =====================")
    sys.exit()
else:
    print("  =====================")
    print("  Сломалось :( Ну вот и нахуй ты сюда нажал? Ошибка 0xPIZDEC, terminating...")
    print("  =====================")
    sys.exit()

# Запуск команды и получение результата
if cmd:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    error = stderr.read().decode("utf-8")
    
    if error:
        print("  =====================")
        print(f"  Ошибка 0xZALUPA {error}, terminating...")
        print("  =====================")
    else:
        print("  =====================")
        print(f"  Ебаться подано, господа! Снапшот создан!")
        print("  =====================")

# Закрытие соединения
ssh.close()
