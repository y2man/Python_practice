#dictionaries are used to store data values in key:value pairs
# dictionaries are ordered, changeable and do not allow duplicates

student = {"name": "john", "age" : 20,"course":"python"}

for key in student.keys():
    print(key)
for value in student.values():
    print(value)  
for key,value in student.items():
    print(key,value)      