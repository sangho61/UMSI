import random
words_list=[]

def ask_q():
    question=input("What is your question?")
    words_list.append(question)
    while not question == "quit":
        if not question[-1] == '?':
            print("I'm sorry, I can only answer questions.")
            question = input("What is your questions?")
        else:
            question = input("What is your questions?")



ask_q()
