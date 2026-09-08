# Employee Management System
# Complete the missing code.
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary
    # Getter
    @property
    def salary(self):
        return self._salary
    
    # Setter
    @salary.setter
    def salary(self, value):
        if value >= 0:
            self._salary = value
        else:
            print("Salary cannot be negative.")
    def work(self):
        print(self.name, "is working.")

# Developer inherits from Employee
class Developer(Employee):
    def work(self):
        print(self.name, "is writing code.")

# Designer inherits from Employee
class Designer(Employee):
    def work(self):
        print(self.name, "is creating designs.")
        
# Create employee objects
developer = Developer("Alice", 5000)
designer = Designer("Bob", 4500)
# Store the objects in a list
employees = [developer, designer]
# Display information
for employee in employees:
    print("Name:", employee.name)
    print("Salary:", employee.salary)
    # Different objects perform work differently
    employee.work()
    print()
