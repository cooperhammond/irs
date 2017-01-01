def center(lst):
    length = len(lst)
    center = -1
    for num in range(0, length):
        if not (num % 2):
            center += 1
    return lst[center]
    
print (center(center([1, 2, [1, 2, 3], 4, 5])))