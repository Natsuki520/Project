class Student:
    def __init__ (self , name , score):
        self.name = name 
        self.score = score

    def add_bonus(self):
        self.score +=5

student1 = Student("Alice" , 85)
student1.add_bonus()
print (student1.name , student1.score)