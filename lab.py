matrix = [[1, 1 ,1],
          [2, 2, 2], 
          [3, 3, 3]]

def in_matrix(e, matrix: [list, tuple]):
    for row in matrix:
        if row.count(e) > 0:
            return True
    return False

a = 1
def do_it():
    global a
    print(a)
    a+=1 
    if a < 10:
        do_it()

do_it()
