import requests
import os
from dotenv import load_dotenv

try: 






    url = "https://jsonplaceholder.typicode.com/posts"
    query = {"userId": 2}
    header = {"autorizaton": " the api buzz","content-type":"application/json"}
    
    response = requests.get(url,params= query,timeout=10)
    
    response.raise_for_status()
    
    data = response.json()
    load_dotenv()
    api_key = os.getenv("AI_API_KEY")
    print(api_key)
    
    header = {"autorization": " this is buzz"}
    
    print("number of data returned are: " ,len(data))
    print("the title of the first box is : ", data[0]['title'])
    
except requests.exceptions.RequestExceptin as error: 
    print(" we got this error: ",error)
    
    
