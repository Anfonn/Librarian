import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.qa_with_sources import load_qa_with_sources_chain 

app = Flask(__name__)
CORS(app)

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    query = data['query']

    os.environ["OPENAI_API_KEY"] = ""

    embedding_function = OpenAIEmbeddings()
    persist_directory=r""
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    retriever = vectordb.as_retriever()
    
    llm= OpenAI(temperature=0)
    chain = load_qa_with_sources_chain(llm=llm, chain_type="map_reduce")

    docs = retriever.get_relevant_documents(query)

    output = chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5001)