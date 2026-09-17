# app/ingest.py
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_index(doc_dir: str, index_path: str = "faiss_index"):
    print(f"正在读取 {doc_dir} 下的文档...")
    # Windows 下读取中文 txt 需要指定 utf-8
    loader = DirectoryLoader(
        doc_dir, glob="**/*.txt", 
        loader_cls=TextLoader, 
        loader_kwargs={'encoding': 'utf-8'}
    )
    documents = loader.load()
    print(f"加载文档: {len(documents)} 个")

    if len(documents) == 0:
        print("警告：没有找到任何文档！请检查 data/benign 文件夹。")
        return

    # 切分文档
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"切分后: {len(chunks)} 块")

    # 向量化
    print("正在加载 Embedding 模型 (BAAI/bge-m3)，首次运行需要下载...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    
    # 存入 FAISS
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)
    print(f"✅ 索引已成功保存至 {index_path} 文件夹！")

if __name__ == "__main__":
    build_index("./data/benign")