import os
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

genai.configure(api_key="AIzaSyBAivfdM7Aj31S3eCnuj3_BxUHN1p7ZHVc")

# Q&A Model 
qa_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="You are a Web Development and DSA instructor. Answer queries in the simplest way possible."
)

# Code Model 
code_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a programming assistant. Explain and write code clearly for beginners."
)

def load_documents(folder_path="notes"):
    docs = []
    filenames = []
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
            docs.append(f.read())
            filenames.append(filename)
    return docs, filenames

documents, doc_names = load_documents()
embedder = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = embedder.encode(documents, convert_to_numpy=True)

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings)

def retrieve_context(query, top_k=1):
    query_vec = embedder.encode([query])
    distances, indices = index.search(np.array(query_vec), top_k)
    return "\n".join([documents[i] for i in indices[0]])

# RAG + LLM Call
def answer_with_context(query, history_list):
    chat_log = ""
    for turn in history_list:
        chat_log += f"User: {turn['user']}\nBot: {turn['bot']}\n"

    context = retrieve_context(query)
    prompt = f"""Use the following notes to answer the query.
Conversation so far:
{chat_log}

Context from notes:
{context}

Current user query: {query}
"""
    response = qa_model.generate_content(prompt)
    return response.text

#  Explainer
def explain_code(code_snippet, language="unspecified"):
    prompt = f"Explain the following {language} code for a beginner:\n\n{code_snippet}"
    response = code_model.generate_content(prompt)  
    return response.text

# Debugger 
def debug_code(code_snippet, language="unspecified"):
    prompt = f"Find and fix any bugs in the following {language} code without changing much of the logic. Explain the errors and give the corrected version:\n\n{code_snippet}"
    response = code_model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("Choose mode:\n1.Q&A\n2. Code Explainer\n3. Code Debugger")
    choice = input("Enter choice: ")

    if choice == "1":
        history = []  
        print("\nAsk your Web Dev/DSA questions. Type 'exit' to quit.\n")

        while True:
            query = input("You: ")
            if query.lower() == "exit":
                print("Session ended.")
                break

            response_text = answer_with_context(query, history)
            print("\nBot:", response_text)
            history.append({"user": query, "bot": response_text})

    elif choice == "2":
        while True:
            code = input("\nPaste your code snippet (or type 'exit' to quit):\n")
            if code.lower() == "exit":
                print("Session ended.")
                break
            lang = input("What language is this? (e.g., HTML, JS, C++): ")
            print("\n--- Explanation ---\n")
            print(explain_code(code, lang))

    elif choice == "3":
        while True:
            code = input("\nPaste your code to debug (or type 'exit' to quit):\n")
            if code.lower() == "exit":
                print("Session ended.")
                break
            lang = input("What language is this? (e.g., Python, Java, C++): ")
            print("\n--- Debugging Result ---\n")
            print(debug_code(code, lang))

    elif choice.lower() == "exit":
        print("Session Ended.")
    else:
        print("Please ask me questions related to DSA or WebDev!! That's my expertise haha.")