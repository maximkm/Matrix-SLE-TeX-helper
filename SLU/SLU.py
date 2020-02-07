from copy import deepcopy as dpc
from math import gcd


def OutPutSluTex(slu, sep, output, dem=''):
    print(f'{dem} ' + '\\left( \\begin{array}{' + 'c' * sep + ('|' if sep != len(slu[0]) else '') + 'c' * (len(slu[0]) - sep) + '}', file=output)
    for i in range(len(slu)):
        print(' & '.join(map(str, slu[i])) + ('\\\\' if i != len(slu) - 1 else ''), file=output)
    print('\\end{array}\\right)', file=output)


def OutPutSlu(slu, sep):
    x = max(map(len, map(str, [slu[i][j] for i in range(len(slu)) for j in range(len(slu[0]))]))) + 1
    for i in range(len(slu)):
        for j in range(len(slu[0])):
            print(f'{str(slu[i][j]).rjust(x)}', end=('|' if j == sep - 1 and sep != len(slu[0]) else ' '))
        print('')


def LastSLU(slu, colName, tr, sep, output, cnt, constRes, dem=''):
    res = False
    for row in range(len(slu)):
        flag = False
        temp = 0
        for col in range(len(slu[row])):
            if slu[row][col] and slu[row][col] != 1:
                temp = slu[row][col]
                flag = True
                break
        if flag:
            for col in range(len(slu[row])):
                if slu[row][col]:
                    if slu[row][col] % temp == 0:
                        slu[row][col] //= temp
                    else:
                        bar = gcd(slu[row][col], temp)
                        slu[row][col] = '\\frac{' + str(slu[row][col]//bar) + '}{' + str(temp//bar) + '}'
                        res = True
    if res:
        OutPutSlu(slu, sep)
        ans = input('save last SLU? ')
        if ans.lower() == 'y':
            if cnt % constRes == 0 and cnt != 0:
                print(f'{dem} \\]\n\\[', file=output)
            if not colName:
                OutPutSluTex(dpc(slu), sep, output, dem)
            else:
                OutPutSluTex(UnionName(dpc(slu), colName, tr), sep, output, dem)


def TransposeSLU(slu):
    a = len(slu)
    b = len(slu[0])
    resSLU = []
    for i in range(b):
        temp = []
        for j in range(a):
            temp.append(slu[j][i])
        resSLU.append(dpc(temp))
    return resSLU


def Action(slu, x, y, z, tr):
    if tr:
        slu = TransposeSLU(slu)
    if z == 'swap':
        slu[x - 1], slu[y - 1] = slu[y - 1], slu[x - 1]
    elif z == '*':
        slu[x - 1] = [item * y for item in slu[x - 1]]
    elif z == '/':
        for item in slu[x - 1]:
            if item % y != 0:
                break
        else:
            slu[x - 1] = [item // y for item in slu[x - 1]]
    else:
        for i in range(len(slu[0])):
            slu[x - 1][i] += z * slu[y - 1][i]
    if tr:
        slu = TransposeSLU(slu)
    return slu


def AddHist(slu, hist, trHist, sepHist, sep, tr):
    if slu != hist[-1]:
        hist.append(dpc(slu))
        trHist.append(tr)
        sepHist.append(sep)


def Shrink(slu, hist, trHist, sepHist, sep, tr):
    for i in range(len(slu)):
        temp = 1
        for j in range(len(slu[0])):
            if slu[i][j] != 0:
                temp = slu[i][j]
                for k in range(j + 1, len(slu[0])):
                    if slu[i][k] != 0:
                        temp = gcd(temp, slu[i][k])
                break
        if temp != 1:
            slu = Action(dpc(slu), i + 1, temp, '/', 0)
    AddHist(slu, hist, trHist, sepHist, sep, tr)
    return slu


def EchelonForm(slu, mode, hist, trHist, sepHist, sep, tr):
    slu = Shrink(dpc(slu), hist, trHist, sepHist, sep, tr)
    row, col = 0, 0
    fav = []
    while row < len(slu) and col < len(slu[0]):
        temp = []
        for i in range(row, len(slu)):
            if slu[i][col] != 0:
                temp.append([slu[i][col], i])
        if temp:
            temp.sort(key=lambda x: abs(x[0]))
            slu = Action(dpc(slu), row + 1, temp[0][1] + 1, 'swap', 0)
        if slu[row][col] != 0:
            if slu[row][col] < 0:
                slu = Action(dpc(slu), row + 1, -1, '*', 0)
            slu = Shrink(dpc(slu), hist, trHist, sepHist, sep, tr)
            fav.append([row, col])
            for i in range(row + 1, len(slu)):
                if slu[i][col] != 0:
                    if slu[i][col] % slu[row][col] == 0:
                        slu = Action(dpc(slu), i + 1, row + 1, -slu[i][col] // slu[row][col], 0)
                    else:
                        idx = slu[row][col] // gcd(slu[i][col], slu[row][col])
                        slu = Action(dpc(slu), i + 1, idx, '*', 0)
                        slu = Action(dpc(slu), i + 1, row + 1, -slu[i][col] // slu[row][col], 0)
                    AddHist(slu, hist, trHist, sepHist, sep, tr)
            row += 1
            col += 1
        else:
            col += 1
        slu = Shrink(dpc(slu), hist, trHist, sepHist, sep, tr)
    if mode:
        fav.reverse()
        for row, col in fav:
            for i in range(row, 0, -1):
                if slu[i - 1][col] != 0:
                    if slu[i - 1][col] % slu[row][col] == 0:
                        slu = Action(dpc(slu), i, row + 1, -slu[i - 1][col] // slu[row][col], 0)
                    else:
                        idx = slu[row][col] // gcd(slu[i - 1][col], slu[row][col])
                        slu = Action(dpc(slu), i, idx, '*', 0)
                        slu = Action(dpc(slu), i, row + 1, -slu[i - 1][col] // slu[row][col], 0)
                    AddHist(slu, hist, trHist, sepHist, sep, tr)
        slu = Shrink(dpc(slu), hist, trHist, sepHist, sep, tr)
    return slu


def FSR(slu, output):
    slu = EchelonForm(dpc(slu), 1, [0], [0], [0], len(slu), 0)
    row, col = 0, 0
    fav, free = [], []
    while row < len(slu) and col < len(slu[0]):
        if slu[row][col] != 0:
            fav.append([row, col])
            row += 1
            col += 1
        else:
            free.append(col)
            col += 1
    if free:
        print('$', end='', file=output)
        free.reverse()
        for num, col in enumerate(free):
            print('--')
            temp = []
            for row, y in fav:
                if slu[row][col] != 0:
                    temp.append(slu[row][y] // gcd(slu[row][y], slu[row][col]))
            res = 1
            if temp:
                res = temp[0]
            for item in temp:
                res = res*item//gcd(res, item)
            temp = [0]*len(slu[0])
            temp[col] = res
            for row, y in fav:
                temp[y] = -slu[row][col]*res//slu[row][y]
            print('\\left( \\begin{array}{c}', file=output)
            for i, item in enumerate(temp):
                print(f'{item}' + '\\\\'*(i != len(temp) - 1), end=(' ' if i != len(temp) - 1 else '\n'), file=output)
                print(item)
            print('\\end{array} \\right)' + ',' * (len(free) - 1 != num), end=('\n' if num != len(free) - 1 else ''), file=output)
            if num == len(free) - 1:
                print('--')
        print('$', file=output)


def SluLoad():
    slu = []
    sep = 0
    colName = []
    with open('input.txt') as file_handler:
        for num, line in enumerate(file_handler):
            temp = list(line.replace('\n', '').split())
            if num == 0:
                sep = len(temp) if '|' not in temp else temp.index('|')
                if not temp[0].replace('-', '').isdigit():
                    if '|' in temp:
                        temp.remove('|')
                    colName = temp
                    continue
            if '|' in temp:
                temp.remove('|')
            temp = [x.replace('|', '') for x in temp]
            slu.append(list(map(int, temp)))
    with open('config.txt') as file_handler:
        res = []
        for num, line in enumerate(file_handler):
            if num == 3:
                break
            res.append(list(line.replace(' ', '').replace('\n', '').split('='))[-1])
    autoPrint, mode, delim = res
    return slu, sep, colName, int(autoPrint), int(mode), delim


def SaveSLU(slu, sep):
    inp = open('input.txt', 'w')
    for i in range(len(slu)):
        for j in range(len(slu[0])):
            print(f'{slu[i][j]}' + (' |' if j == sep - 1 != len(slu[0]) - 1 and i == 0 else ''), end='\t', file=inp)
        print(file=inp)
    inp.close()


def UnionName(slu, colName, tr):
    if tr:
        for i in range(len(colName)):
            slu[i] = [colName[i]] + slu[i]
        return slu
    else:
        return [colName] + slu


def main():
    slu, sep, colName, autoPrint, mode, delim = SluLoad()
    post = ''
    trans = False
    if len(slu) == 0:
        print('bad SLU, try again')
        return 0
    print(f'SLU load complete, mode =', ('col' if mode else 'row'))
    print('input \'help\' for help')
    hist = [dpc(slu)]
    trHist = [trans]
    sepHist = [sep]
    while post != 'exit':
        if autoPrint:
            OutPutSlu(slu, sep)
        posts = input(f'step {len(hist)}: ').replace(' ', '').lower().split(',')
        for post in posts:
            if post == 'p':
                OutPutSlu(slu, sep)
            elif post == 'pt':
                num = 0
                cnt = 0
                constRes = ''
                while not constRes.isdigit():
                    constRes = input('How many slu one row?: ')
                constRes = int(constRes)
                output = open('output.txt', 'w')
                print('\\[', file=output)
                for sepX, trX, sluX in zip(sepHist, trHist, hist):
                    num += 1
                    OutPutSlu(sluX, sepX)
                    ans = input(f'Save this matrix {num}/{len(hist)}? (y/n): ')
                    if ans.lower() == 'y':
                        if cnt % constRes == 0 and cnt != 0:
                            print(f'{delim} \\]\n\\[', file=output)
                        if not colName:
                            OutPutSluTex(dpc(sluX), sepX + trX, output, delim if cnt != 0 and cnt % constRes != 0 else '')
                        else:
                            OutPutSluTex(UnionName(dpc(sluX), colName, trX), sepX + trX, output, delim if cnt != 0 and cnt % constRes != 0 else '')
                        cnt += 1
                    if num == len(sepHist):
                        LastSLU(dpc(sluX), colName, trX, sepX + trX, output, cnt, constRes, delim if cnt != 0 and cnt % constRes != 0 else '')
                print('\\]', file=output)
                output.close()
            elif post == 'back':
                if len(hist) != 1:
                    hist.pop()
                    slu = dpc(hist[-1])
            elif post == 'help':
                print('(i)(j) —— swap row i and row j')
                print('(i)*(k) —— elems row i * num k')
                print('(i)/(k) —— elems row i / num k')
                print('(i)+-k(j) —— row i +- k * row j')
                print('p —— print SLU')
                print('pt —— print history LaTeX code SLU')
                print('back —— cancel last action')
                print('tr —— transpose matrix')
                print('mode —— поменять вид преобразований (строки/столбцы)')
                print('form —— ступенчатый вид')
                print('best form —— улучшенный ступенчатый вид')
                print('fsr —— код ФСР LaTeX')
                print('shrink —— упростить СЛУ')
                print('save —— сохранить матрицу в input.txt')
                print('exit —— завершить программу')
            elif post == 'tr':
                if sep == len(slu[0]):
                    trans = False if trans else True
                    slu = TransposeSLU(slu)
                    sep = len(slu[0])
                    hist.append(dpc(slu))
                    trHist.append(trans)
                    sepHist.append(sep)
                else:
                    print('delete partition')
            elif post == 'mode':
                mode = (mode + 1) % 2
                print(f'now mode =', ('col' if mode else 'row'))
            elif post == 'save':
                if trans:
                    SaveSLU(slu, sep)
                else:
                    SaveSLU(UnionName(dpc(slu), colName, trans), sep)
            elif post == 'form':
                slu = EchelonForm(slu, 0, hist, trHist, sepHist, sep, trans)
            elif post == 'bestform':
                slu = EchelonForm(slu, 1, hist, trHist, sepHist, sep, trans)
            elif post == 'shrink':
                slu = Shrink(dpc(slu), hist, trHist, sepHist, sep, trans)
            elif post == 'fsr':
                output = open('outputFSR.txt', 'w')
                FSR(dpc(slu), output)
                output.close()
            else:
                try:
                    temp = post[post.find(')') + 1:post.rfind('(')]
                    if temp == '-':
                        temp = -1
                    elif temp == '+':
                        temp = 1
                    if temp == '*':
                        slu = Action(dpc(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]), '*', mode)
                    elif temp == '/':
                        slu = Action(dpc(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]), '/', mode)
                    elif temp != '':
                        slu = Action(dpc(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]), int(temp), mode)
                    else:
                        slu = Action(dpc(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]), 'swap', mode)
                        if mode and colName:
                            x = int(post[1:post.find(')')])
                            y = int(post[post.rfind('(') + 1:-1])
                            colName[x - 1], colName[y - 1] = colName[y - 1], colName[x - 1]
                    if hist[-1] != slu:
                        hist.append(dpc(slu))
                        trHist.append(trans)
                        sepHist.append(sep)
                except BaseException:
                    slu = dpc(hist[-1])


if __name__ == '__main__':
    main()
