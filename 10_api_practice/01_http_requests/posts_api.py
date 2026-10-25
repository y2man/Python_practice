import os
import requests
from dotenv import load_dotenv


try: 
    url = "https://jsonplaceholder.typicode.com/posts"
    param= {"userId": 2}
    
    response = requests.get(url,params=param,timeout=10)
    
    response.raise_for_status()
    load_dotenv()
    apikey = os.getenv("AI_API_KEY")
    
    data = response.json()
    
    print("The number of posts are: ",len(data))
    print("the fist post title is ",data[0]["title"])
    
    
    
    
    
    
except requests.exceptions.RequestException as error: 
    print("The request got this error: ", error)