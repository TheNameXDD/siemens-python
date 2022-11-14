import snap7 
import snap7.client as c
from snap7.util import *
from snap7.snap7types import *

def WriteMemory(plc, byte, bit, datatype, value): #Функция с аргументами чтобы составить запрос
    result = plc.read_area(snap7.types.Areas.MK, 0, byte, datatype) #MK - область памяти к которой обращаемся. DB - база данных, PE - входы, PA - выходы, MK - таблица тегов
    if datatype == S7WLBit: #Проверяем к какой области памяти мы обращаемся
        set_bool(result, 0, bit, value) #
    plc.write_area(snap7.types.Areas.MK, 0, byte, result) #Команда которая отправляется на контроллер S7-1200

if __name__ == "__main__":
    plc = c.Client() #Создание виртуального клиента
    plc.connect('192.168.0.1', 0, 1) #Подключение к контроллеру по адресу
    WriteMemory(plc, 0, 0, S7WLBit, 1)  #Делаем запрос на def WriteMemory и отправляем туда данные которые необходимо отправить на контроллер. Первый аргумент - адрес контроллера, второй - это номер байта
                                        #третий - это номер бита в байте, четвертый - это тип памяти к которой мы обращаемся (BOOL тип), пятый - это наше значение которое будет присвоено
