import os
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
        print("Error: GROQ_API_KEY was not found in .env")
        
else: 
                
        def load_document(file_path):

            try: 
            
            
                with open(file_path,"r",encoding="utf-8") as file: 
                    
                    
                   content = file.read()
                
                if not content.strip():
                    return None

                return content


            except FileNotFoundError:
                return None

        def send_request(document,question,api_key):
            if not api_key:
                    print("Error: GROQ_API_KEY was not found in .env")
                    return None
            messages= build_messages(document, question)
            
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            data = {
                    "model": "openai/gpt-oss-20b",
                    "messages": messages,
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
                return result
        
            except requests.exceptions.RequestException as error:
                    
            
                    if error.response is not None:
                        print("Server response:", error.response.text)
            
                    return None
            
            except (KeyError, IndexError, TypeError, ValueError) as error:
                    print("Unexpected API response:", error)
                    return None

            
        def build_messages(document, question):
            messages = [
                {
                    "role": "system",
                    "content": "Your instracion is 1.Answer using only the supplied document. 2.If the answer isn't in the document, say that the document doesn't provide the answer. 3.Never invent information."
                    

                },
                {
                    "role": "user",
                    "content": f"document: {document}  question: {question}"
                }
            ]

            return messages


        def extract_answer(result):
            if not isinstance(result, dict):
                return "No answer available"
            

            choices = result.get("choices", [])
            
            if isinstance(choices,list) and len(choices)>=1:
                
                choice = choices[0] if choices else {}
                if isinstance(choice,dict):
                
                    message = choice.get("message", {})
                    if isinstance(message,dict):
                        content = message.get("content", "")
                        

                        if isinstance(content,str) and content.strip():
                            return content
                        else: return "No answer available"
                    else: return "No answer available"
                else: return "No answer available"
            else: return "No answer available"


        file_path = r"C:\Users\lenovo\Downloads\Python_practice\13_ai_and_llm_integration\04_ai_document_assistant\documents\sample.txt"

        document = load_document(file_path)

        if document is not None:
         
            while True:
                question = str(input("Ask question :  "))
                
                if question.lower().strip()=="exit":
                    break
                elif question.lower().strip()=="":
                    print("Please enter your question")
                else:
                
                    result= send_request(document,question,api_key)
                    

                    if result:
                        print(f"AI Answer: {extract_answer(result)}")
                    else:
                        print("Sorry, I couldn't get an answer from the AI service. Please try again.")

            
        else:
            print("Could not load the document.")
            
        

