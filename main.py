# -*- coding: utf-8 -*-

# Необходимо для вывода

from get_data_arrays import output

# Стартовая точка программы
if __name__ == "__main__":
    from get_data_arrays import nodes_quantity as uz_num, nodes_fin as nodes_fin, forces_fin as usiliya, pinning
# nodes_quantity - количество узлов
# nodes_fin - координаты узлов
# forces_fin - список сил по узлам

# Функция добавления необходимых данных по элементам
def adding():
    temp = []
    for i in range(0, uz_num - 1):
        print('Значение для элемента ', i)
        temp.append(int(input()))
    print('Итоговый результат:', temp)
    des = input("Хотите изменить? (Да/Нет)")
    if des == "Да":
        temp = adding()
    return temp

print('Определим недостающие данные.')
print('Warning! Все данные вводятся исключительно в численном формате и не должны содержать иных символов. '
      'В противном случае, разработчик не несет ответственности за результаты вычисления.')
print('1. Задайте длины элементов.')
#el_length = adding()
el_length=[2,1,2,3]
print('2. Задайте жёсткости элементов.')
#gestkosti = adding()
gestkosti=[2,1,2,3]
# Выдадим юзеру его чертежи

balka = []
def chertezUzlov():
    print('Расчётная схема балки в масштабе')
    for i in range(1, uz_num+1):
        if usiliya[i-1] == 0:
            balka.append('-'*el_length[i-2])
        else:
            balka.append('-'*el_length[i-2]+ ' F = '+ str(usiliya[i-1]))
    balka[0] = "||"
    balka.append("||")
    print(balka)
    return balka
chertezUzlov()

# обьявление вспомогательной матрицы
arrayG = [[1, -1],
          [-1, 1]]

# формируем заготовку для массива матриц жесткостей
arrayGes = []
for i in range(uz_num-1):
    arrayGes.append([])
    for j in range(len(arrayG)):
        arrayGes[i].append([])
# на выходе получим [  [ [], [] ],  [ [], [] ],
#                      [ [], [] ],  [ [], [] ]  ]

# считаем матрицу жесткостей элементов
def makeMatricaGestcosti():
    for i in range(uz_num-1):
        for j in range(len(arrayG)):
            for k in range(len(arrayG[j])):
                arrayGes[i][j].append(float(gestkosti[i]) * float(arrayG[j][k]))
    return arrayGes

makeMatricaGestcosti()
# выводим матрицы жесткостей элементов
def vivod(arrayGes):
    k = 0
    for i in range(len(arrayGes)):
        for j in range(len(arrayGes[i])):
            if k % 2 == 0:
                print('Матрица жесткости ', i + 1, '-го элемента: \n', arrayGes[i][j])
                k += 1
            else:
                print('', arrayGes[i][j])
        k = 0

vivod(arrayGes)
print('')

#Делаем вспомогательный список
matGes = []
for i in range(len(gestkosti) + 1):
    matGes.append([])

# считаем матрицу жесткости системы
def makeMatricaGestcostiSistemi():
    #Задаём первый элемент
    matGes[0].append(arrayGes[0][0][0])
    for i in range(len(gestkosti) + 1):
        for j in range(len(gestkosti) + 1):
            #Если элемент на диагонали
            if i == j and i != 0 and i != len(gestkosti):
                matGes[i].append(arrayGes[i][0][0] + arrayGes[i - 1][0][0])
            #Если выше диагонали
            elif j == i - 1 and i != 0 and i != len(gestkosti) + 1:
                matGes[i].append(arrayGes[i - 1][0][1])
            #Если ниже диагонали
            elif j == i + 1 and i != len(gestkosti) + 1:
                matGes[i].append(arrayGes[i][0][1])
            elif j != i and j != -1 and i != -1:
                matGes[i].append(0)
    matGes[-1].append(arrayGes[-1][0][0])
    return matGes


makeMatricaGestcostiSistemi()

print('Матрица жесткости системы')
for i in range(len(matGes)):
    print(matGes[i])
print('')

def vvodGranichnihUsloviy():
    for i in range(len(matGes)):
        for j in range(len(matGes[i])):
            if j == 0 or j == len(matGes) - 1 or i == 0 or i == len(matGes) - 1:
                matGes[i][j] = 0
    matGes[0][0] = 1
    matGes[-1][-1] = 1
    return matGes

vvodGranichnihUsloviy()

print('Матрица жесткости системы с граничными условиями')
for i in range(len(matGes)):
    print(matGes[i])
print('')

print('\n' + 'Конец моей части')

print('Фалько начало')

UzlovidePeremesheniya= []

def matrichnoeUravnenie():
    for i in range(len(gestkosti) + 1):
        UzlovidePeremesheniya.append('U' + str(i + 1))
        print(str(matGes[i]) + ' * ' + str(UzlovidePeremesheniya[i]) + ' = ' + str(usiliya[i]))


print('Матричное уравнение')
matrichnoeUravnenie()
print('')

arrayReshenie = []
arr1 = []
arr = []
for i in range(len(el_length) - 2):
    arr.append([])



def makeArr():
    for i in range(1, len(el_length) - 1):
        for j in range(1, len(el_length) - 1):
            for k in range(1):
                arr[i - 1].append(matGes[i][j])
    return arr


makeArr()

arrU = []


def makeArrU():
    for i in range(1, len(el_length) - 1):
        arrU.append(el_length[i])
    return arrU


makeArrU()

print('Упрощаем для решения методом Гаусса (этап 1) - убираем лишнее для наглядности')
print('Убираем нулевые строки и столбцы для уменьшения количества действий')
for i in range(len(arr)):
    print(str(arr[i]) + ' = ' + str(arrU[i]))
print('')

m=[]
def mnogitel(i, elem):
    for j in range(len(elem)):
        if i == j:
            m = elem[i - 1][j] / elem[i][j]
    return m

def vopros(text):
    m = ''
    while m != '1' and m != '0' and m.lower() != 'да' and m.lower() != 'нет':
        m = input(text)
    return m

okr = False
m = vopros('Хотите округлить результаты? ')
if m == '1' or m.lower() == 'да':
    okr = True
    DrobnChast = None
    while DrobnChast == None:
        DrobnChast = input('Сколько знаков оставить после запятой? ')

def roundNum(num, DrobnChast):
    num = round(num * 10 ** int(DrobnChast))/(10 ** int(DrobnChast))
    return num

print('Упрощаем для решения методом Гаусса (этап 2)')

def triangleArray():
    for i in range(len(arr) - 1, 0, -1):
        mn = mnogitel(i, arr)
        b = float(arrU[i - 1]) - float(arrU[i]) * mn
        if okr is True:
            b = roundNum(b, DrobnChast)
        arrU[i - 1] = b
        for j in range(len(arr[i]) - 1, -1, -1):
            a = arr[i - 1][j] - arr[i][j] * mn
            if okr is True:
                a = roundNum(a, DrobnChast)
            arr[i - 1][j] = a
    return arr

triangleArray()

for i in range(len(arr)):
    print(str(arr[i]) + ' = ' + str(arrU[i]))
print('')


def intU():
    for i in range(len(arrU)):
        arrU[i] = float(arrU[i])
    return arrU


intU()

resh = 0
uLoc = 0
U = []


def reshenieSlay():
    arrayReshenie.append(0)
    for i in range(len(arrU)):
        for j in range(len(arrU)):
            if i == j and i == 0:
                resh = arrU[i] / arr[i][j]
                if okr is True:
                    resh = roundNum(resh, DrobnChast)
                uLoc = resh
            elif i == j:
                resh = (arrU[i] - uLoc * arr[i][j - 1]) / arr[i][j]
                if okr is True:
                    resh = roundNum(resh, DrobnChast)
                uLoc = resh
        arrayReshenie.append(resh)
    arrayReshenie.append(0)
    return arrayReshenie


U = reshenieSlay()
print('Столбец возможных перемещений')
print(U)
print('')

N = []

for i in range(len(gestkosti)):
    N.append([])

# Число узлов, число элментов, массив координат узлов, массив длин элементов
length=[]
def uzlovie_coordinates():
    with open("input File.txt", "r") as f:
        for line in f:
            if line[slice(0,4)] == 'GRID':
                arr = line.split(' ')
                arr = [x for x in arr if x != '']
                el_length = arr[2]
                L1 = el_length.split('.')
                if L1[1] == '':
                    L1[1] = '0'
                el_length = int(L1[0]) + int(L1[1])/10**(len(L1[1]))
                length.append(el_length)
    return length

def masssiveFunFormForEachElementInTochka(x):
    for i in range(len(gestkosti)):
        N[i] = []
    for i in range(len(gestkosti)):
        N1 = 1 - x / float(el_length[i])
        N2 = x / float(el_length[i])
        N[i].append(N1)
        N[i].append(N2)
    return N


# PeremeshenieElementaVTochke = 0


def sluchPeremeshenie():
    PeremeshenieElementaVTochke = 0
    element = None
    while element == None:
        element = input('Введите номер элемента от 1 до ' + str(len(gestkosti)) + ' ')
        if element != None:
            element = int(element)
            if element <= len(gestkosti) and element > 0:
                m = '1'
                while m == '1':
                    x = input('Введите координату от 0 до 1 в ' + str(element) + ' элементе в долях от ' + str(
                        el_length[element - 1]) + ' м ')
                    x = float(x)
                    if x <= 1 and x >= 0:
                        masssiveFunFormForEachElementInTochka(x)
                        PeremeshenieElementaVTochke = N[element - 1][0] * U[element - 1] + N[element - 1][1] * U[
                            element]
                        if okr is True:
                            PeremeshenieElementaVTochke = roundNum(PeremeshenieElementaVTochke, DrobnChast)
                        print(PeremeshenieElementaVTochke)
                        m = vopros('Хотите снова найти перемещение в ' + str(element) + ' элементе? ')
                    else:
                        print('Непрвильная координата\n')
            else:
                print('Непрвильный номер элемента\n')
    return PeremeshenieElementaVTochke


m = vopros('Хотите найти перемещение в указанной точке? ')
if m == '1' or m.lower() == 'да':
    m = '1'
    while m == '1' or m.lower() == 'да':
        sluchPeremeshenie()
        m = vopros('Хотите снова найти перемещение в указанной точке? ')

print('')

arrT = []

rasDef = False
maxDef = False


def skolkoTochek(rasDef, maxDef):
    kolT = None
    while kolT == None:
        if rasDef is True:
            kolT = input('Сколько точек хотите рассмотреть в каждом элементе? (Не считая узловых точек) ')
        elif maxDef is True:
            kolT = input('На сколько точек хотите разбить элементы? ')
    for i in range(int(kolT) + 2):
        arrT.append(1 / (int(kolT) + 1) * i)
    return arrT


arrRas = []
for i in range(len(gestkosti)):
    arrRas.append([])


def makeArrayRaspredelenya():
    skolkoTochek(True, False)
    for i in range(len(gestkosti)):
        for j in range(len(arrT)):
            masssiveFunFormForEachElementInTochka(arrT[j])
            PeremeshenieElementaVTochke = N[i][0] * U[i] + N[i][1] * U[i + 1]
            if okr is True:
                PeremeshenieElementaVTochke = roundNum(PeremeshenieElementaVTochke, DrobnChast)
            arrRas[i].append(PeremeshenieElementaVTochke)
    return arrRas


print('\n' + 'Конец решения')