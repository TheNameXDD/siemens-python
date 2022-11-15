import snap7 
import snap7.client as c
from snap7.util import *
from snap7.snap7types import *

#Адреса ПЛК
plc_address = '192.168.0.1'
plc_rack = 0
plc_slot = 1

def WriteMemory(plc, byte, bit, datatype, value): #Функция с аргументами чтобы составить запрос
    result = plc.read_area(snap7.types.Areas.MK, 0, byte, datatype) #MK - область памяти к которой обращаемся. DB - база данных, PE - входы, PA - выходы, MK - таблица тегов, TM - таймер, CT - счетчик
    if datatype == S7WLBit: #Проверяем к какой области памяти мы обращаемся
        set_bool(result, 0, bit, value)
    else:
        return None
    plc.write_area(snap7.types.Areas.MK, 0, byte, result) #Команда которая отправляется на контроллер S7-1200

def ReadMemory(plc, byte, bit, datatype): #Функция с аргументами чтобы получить данные о состоянии памяти контроллера
    result = plc.read_area(snap7.types.Areas.MK, 0, byte, datatype) 
    if datatype == S7WLBit:
        return get_bool(result, byte, bit) #Возвращает TRUE/FALSE
    else:
        return None
     

if __name__ == "__main__":
    plc = c.Client() #Создание виртуального клиента
    plc.connect(plc_address, plc_rack, plc_slot) #Подключение к контроллеру по адресу
    connected = plc.get_connected() #Результат подключения к PLC
    print("Connection to PLC is:", connected)
    WriteMemory(plc, 0, 0, S7WLBit, 1)  #Делаем запрос на def WriteMemory и отправляем туда данные которые необходимо отправить на контроллер. Первый аргумент - адрес контроллера, второй - это номер байта
    #третий - это номер бита в байте, четвертый - это тип памяти к которой мы обращаемся (BOOL тип), пятый - это наше значение которое будет присвоено
    CurrentBit = ReadMemory(plc, 0, 0, S7WLBit)  #Получает данные о состоянии М0.0 в таблице тегов
    print("Current bit state is:", CurrentBit)

    #Получаем данные о состоянии контроллера (Run, Stop, Error)
    state = plc.get_cpu_state()
    print('State:', state)
