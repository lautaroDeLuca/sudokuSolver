def solve(sud):
    find = findBlank(sud)
    if not find:
        return True
    for x in range(1, 10):
        if validMatch(sud, x, find):
            sud[find[0]][find[1]] = x
            if solve(sud):
                return True
            sud[find[0]][find[1]] = 0
    return False

def validMatch(sud, num, pos):
    if checkRow(pos, sud, num) == False:
            return False
    if checkColumn(pos, sud, num) == False:
            return False
    if checkBox(pos, sud, num) == False:
            return False    
    return True                 

def checkRow(cor, sud, num):
    for x in range(len(sud[0])):
        if num == sud[cor[0]][x]:
            return False
    return True

def checkColumn(cor, sud, num):
    for x in range(9):
        if num == sud[x][cor[1]]:
            return False
    return True

def checkBox(cor, sud, num):
    cboxx = cor[0] // 3
    cboxy = cor[1] // 3

    for i in range(cboxx * 3, cboxx * 3 +3):
        for j in range(cboxy * 3, cboxy*3 + 3):
            if sud[i][j] == num:
                return False
    return True    

def findBlank(sud):
    for x in range(len(sud)):
        for y in range(len(sud[0])):
            if sud[x][y] == 0:
                return x, y

def printSudoku(sud):
    for x in range(len(sud)):
        if x % 3 == 0 and x!=0:
            print('----------------------')
        for y in range(len(sud[0])):
            print (sud[x][y], end=' ')
            if y == 2 or y == 5:
                print('| ', end='')
            if y == 8 and y!=0:
                print('')

