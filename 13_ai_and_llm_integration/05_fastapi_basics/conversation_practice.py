# test 

conversations= {"chat_123": []}

conversations["chat_123"].append({"role":"user",
                                  "content":"Hello!"})
conversations["chat_123"].append({"role":"assistant","content":"Hi! How can I help?"})

messages= conversations["chat_123"]
messages.append({"role":"user","content":"What is my name?"})
print(messages)

print(conversations)
