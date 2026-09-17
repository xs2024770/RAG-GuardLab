# app/chain.py
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def build_rag_chain(index_path: str = "faiss_index"):
    print("正在加载索引...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    vectorstore = FAISS.load_local(
        index_path, embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    print("正在连接 Ollama 本地模型...")
    # 注意：这里已经改回 1.5b 小模型
    llm = Ollama(model="qwen2:1.5b", temperature=0)

    prompt = ChatPromptTemplate.from_template("""
你是一个知识库助手。请根据以下材料回答问题。
如果材料中没有相关信息，直接说明不知道。

〖材料〗
{context}

〖问题〗
{question}
""")

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )
    return rag_chain, retriever

if __name__ == "__main__":
    chain, _ = build_rag_chain()
    print("正在提问...")
    answer = chain.invoke("试用期是多久？")
    print("\n=== 模型回答 ===")
    print(answer)
