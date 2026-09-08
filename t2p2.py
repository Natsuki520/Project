items = ["apple" ,"milk", "bread" , "eggs"]
count1 = len(items)
aq=0
a=0
for i in items:
    print (i)
    if items[aq] == "milk":
        a+=1
    aq+=1
print ("Number of items",count1)
if a == 1:
    print("milk is on the list")
else :
    print("milk is not on the list")