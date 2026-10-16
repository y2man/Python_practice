class animal:
    
    code = "this is the animal code"
    def __init__(self,name,age,gender,grade):
        self.name= name
        self.age = age
        self.gender = gender
        self.grade = grade
        
animal = animal("yisak",21,"male",3.65)

print(animal.name)


class dog(animal):
    def __init__(self ,food,drink):
        self.food= food
        self.drink = drink
       
        
dog = dog()

result = dog.code;

print(result)
        