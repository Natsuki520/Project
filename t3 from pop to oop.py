class Student:
    def __init__ (self , name , score):
        self.name = name 
        self.score = score
    
    def display_info(self):
        print ("name:" , self.name , "          score:" , self.score)
    
    @property
    def calculate_grades(self):
        if self.score >=85:
            return "A"
        elif self.score >=75:
            return "B"
        elif self.score >=60:
            return "C"
        else :
            return "D"
    
    def pass_check(self):
        if self.score >= 60:
            return "Pass"
        else :
            return "Fail"
        
    def generate_report(self):
        print("----------report----------")
        self.display_info()
        print ("Your final grade:" , self.calculate_grades)
        print ("Pass or Fail:" , self.pass_check())

try:
    name1 = input("input name:")
    score1 = int(input("input score:"))
    student1 = Student (name1 , score1)
    student1.generate_report()

except ValueError:
    print ("please input correct score!")
