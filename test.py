mylist = [6,1,2,4,8]

index_min = min(range(len(mylist)), key=mylist.__getitem__)

print(index_min)
