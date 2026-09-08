score = {"Alice":92,"Bob":76,"charlie":58,"David":84}
count1 = 4
for name,num in score.items():
    if count1 == 0:
         break
    if 0 <= num <= 100:
            if num >= 90:
                print(name,":excellent")
            elif num >= 60:
                print(name,":pass")
            else:
                print(name,":fail")
    else:
        print("Score must be 0~100")
    count1-=1


        