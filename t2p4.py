import random
num = random.randint(1,100)
while (1) :
    try :
        innum = int(input("Guess a number from 1 to 100 :"))
        if innum > 100 or innum < 1 :
            print("Please input a number from 1 to 100")
            continue
        if innum > num :
            print("too high")
            continue
        elif innum < num :
            print("too low")
            continue
        elif innum == num :
            print ("correct!")
            break
        
    except ValueError :
        print("Please input an int number from 1 to 100")


