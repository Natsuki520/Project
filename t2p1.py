while 1:
    try :
        number = int(input("please input your number"))
        if number > 0:
            print("positive number")
        elif number == 0:
            print("zero")
        else :
            print("negative number")
        if number % 2 == 0:
            print("even number")
        else :
            print("odd number")
        a = input("press anything to continue , exit please press X")
        if a == "X" or a == "x":
            break
    except ValueError:
        print("Error! Please input integer only.")
        a = input("press anything to continue , exit please press X")
        if a == "X" or a == "x":
            break
