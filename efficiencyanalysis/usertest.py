

revin = [4,4,3,4,4,2,3,3,4,3]
fokko = [3,4,3,4,4,2,2,2,3,3]
luuk =  [3,2,3,1,4,2,3,4,4,1]
stef =  [3,2,3,1,2,3,4,4,3,3]
hugo =  [3,2,3,2,3,3,1,3,3,2]
def calcSus(arr):
    if(len(arr)!=10):
        raise Exception("array length incorrect, can not calc SUS score")
    score = 0
    for i in range(0,10):
        if i%2 ==0:
            score = score +arr[i]-1
        else:
            score = score + (5-arr[i])
    return score*2.5

r= calcSus(revin)
f= calcSus(fokko)
l = calcSus(luuk)
s = calcSus(stef)
h = calcSus(hugo)
print(r)
print(f)
print(l)
print(s)
print(h)