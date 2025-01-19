def chek_arifm(mas):
    r1=(mas[0] - mas[1])
    r2=(mas[1] - mas[2])
    r3=(mas[2] - mas[3])
    if r1 == r2 == r3:
        return True
    else:
        return False
def sq(mas):
    if mas[0]**2 > mas[1]*mas[2]*mas[3]:
        return True
    return False

with open('1.txt', 'r') as f:
    s = f.readlines()
    count = 0
    for i in s:
        mas = list(map(int, i.strip().split('\t')))
        mas.sort(reverse=True)
        print(mas)
        if chek_arifm(mas) or sq(mas):
            count += 1
    
    print(count)