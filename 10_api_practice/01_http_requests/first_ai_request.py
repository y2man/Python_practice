
import os
import json
import requests
from dotenv import load_dotenv
def main():
    messages = load_messages()
                
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    while True:
    
        question = get_user_input()
        
        if question.lower().strip()=="/reset":
            messages = reset_messages()
        elif question.lower().strip()=="exit":
            break
        else:
            
            
            check = ask_ai(messages,api_key,question)
            
            
            if check:
                 save_messages(messages)
                 print(f"AI:   {check}")
            else: print("request was  unsuccessfull")
                
            
           
            
    
    
            

                

           
def get_user_input():
   question = input("\nAsk me anything or (enter /reset to reset the message or enter exit to exit the sytem):  ")
   return question
def save_messages(messages): 
    
        
            with open("data.json", "w") as file:
                json.dump(messages, file)
                            
                            
                        
   
def reset_messages(): 
    messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ] 
    with open("data.json", "w") as file:
        json.dump(messages, file)
        print("Conversation reset")
    return messages
    

def ask_ai(messages, api_key, question):
    if not api_key:
        print("Error: GROQ_API_KEY was not found in .env")
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Make a temporary copy of the conversation
    temporary_messages = messages.copy()

    # Add the current question to the temporary copy
    temporary_messages.append({
        "role": "user",
        "content": question
    })

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": temporary_messages,
        "max_completion_tokens": 2048,
        "include_reasoning": False,
        "reasoning_effort": "low"
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        answer = result["choices"][0]["message"].get("content")

        # Don't update the original history if there's no answer
        if not answer:
            print("The API returned an empty answer.")
            return None

        # Update the original conversation only after success
        messages.append({
            "role": "user",
            "content": question
        })

        messages.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)

        if error.response is not None:
            print("Server response:", error.response.text)

        return None

    except (KeyError, IndexError, TypeError, ValueError) as error:
        print("Unexpected API response:", error)
        return None

def load_messages():
     if os.path.exists("data.json"):
        try:
            with open("data.json", "r") as file:
                messages = json.load(file)
            return messages


        except json.JSONDecodeError:
            print("Invalid JSON file!")
            messages = [
                                 {
                                     "role": "system",
                                     "content": "You are a helpful assistant."
                                 }
                             ] 
            return messages
                     
     else:
         print ("the file doesn't exitst")
         messages = [
                     {
                         "role": "system",
                         "content": "You are a helpful assistant."
                     }
                 ] 
         return messages
         
    
if __name__ == "__main__":
    main()
    
    




    
    
    
   

            