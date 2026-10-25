import json


tasks = []

def add_task(tasks, title):
    
    
    new_task = {"title":title,"completed_status": False}
    if title.strip()=="":
        print("Please enter the title ")
    else: 
    

        tasks.append(new_task)
        save_tasks(tasks)
def update_task(tasks):
    try: 
        
        update = int(input("Which task you went to complete?: "))
        if update<=len(tasks) and update>0:
            
        
         tasks[update-1]["completed_status"]=True
         save_tasks(tasks)
         print("The task has been updated!")
        
        else: print("This task hasn't added yet!")
            
    except ValueError: 
        print("Please enter valid number only!")
        
def view_tasks(tasks):
    counter =0
    
    if tasks: 
     for task in tasks:
        print(f"{counter+1}. title: {task['title']}   completed status: {"Completed" if task['completed_status'] else "not Completed! "}")
        counter+=1
    else: print("The taks are empity!")
    
def save_tasks(tasks):

    
        with open("tasks.json","w") as file: 
            json.dump(tasks,file)


    
def load_tasks():
    try: 
    
        with open("tasks.json","r") as file:
            result = json.load(file)
        return result   
        
    except FileNotFoundError:
            print("The file is doesn't exist!")
            return []
    except json.JSONDecodeError:
            print("the JSON file has been corrupted")
            return []
def delete_task(tasks):
    try: 
        
        delete = int(input("Enter the task number you went to delete: "))
        if delete<=len(tasks) and delete>0:
            
        
         del tasks[delete-1]
         save_tasks(tasks)
         print("The task has been deleted!")
        
        else: print("This task hasn't added yet!")
            
    except ValueError: 
        print("Please enter valid number only!")
    
tasks = load_tasks()
while True:
    
 try: 
     print("Welcome to Task Manager!")
     print("Please choose what you went to do!")
     print("for Adding Tasks Enter 1")
     print("for view Tasks Enter 2")
     print("for update Tasks Enter 3")
     print("for delete Tasks Enter 4")
     print("for Exist The System Enter 5")
     choice = int(input("Enter your coice: "))
     if choice==1 :
         title = str(input("Enter the title of the task: "))
        
         
         add_task(tasks,title)
     elif choice==2:
         view_tasks(tasks)
         
     elif choice==3:
        update_task(tasks)
     elif choice==4:
        delete_task(tasks)
    
         
     elif choice ==5:
         print("You are successfully exit the System!")
         save_tasks(tasks)
         break
     
     else: print("Please enter a number with range of 1-5 only!")
        
        
 except ValueError:
     print("Please Enter valid number")
    