r = []
def f(target):
    list = [3,3,3,3,3,3,3,3,3,3]
    for x in range(len(list) - 1):
        if len(list) < 2: break
        if list[x] + list[x + 1] == target:
            k = [x, x+1]
            r.append(k)
    return(r)
print(min(f(6)))