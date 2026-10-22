
import os
import json

file_path = "C:\\Users\\lenovo\\Downloads\\Python_practice\\05_file_handling\\test1.txt"

# if os.path.exists(file_path):
#     print("The file exists")
#     if os.path.isfile(file_path):
#         print("the path is a file")
#     elif os.path.isdir(file_path):
#         print("the path is a directory")    
# else:
#     print("The file doesn't exist")

# file_data = "This is the created file data"

# with open(file_path,"w") as file:
    
#     file.write(file_data);
#     print("the file has been created successfully")



# ithems = {"ithem1": 10,"ithem2":20 , "ithem3":30}

# with open(file_path,"w") as file:
#     json.dump(ithems,file)
#     print("the json has been created successfully")



print("Current working directory:", os.getcwd())

with open("test2.txt", "r") as file:
    content = file.read()
    print(content)



