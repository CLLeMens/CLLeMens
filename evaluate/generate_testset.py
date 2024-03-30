import pandas as pd
from pathlib import Path
from CLLeMensLangchain.vectordbs.faiss import faissDB
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# Read the testset
df = pd.read_excel('testset.xlsx')

# Create the 'data_samples' dictionary structure
data_samples = {
    'question': df['Question'].tolist(),
    'answer': df['Answer'].tolist(),
    'contexts': df['Contexts'].apply(lambda x: [x] if pd.notna(x) else []).tolist(),
    'ground_truth': df['Ground Truth'].tolist()
}
BASE_DIR = Path(__file__).resolve().parent.parent.joinpath('CLLeMensWebServer')
print(BASE_DIR)

EvalDB = faissDB(base_dir=BASE_DIR)

# Check if all Keys have the same amount of elements
lengths = [len(value) for value in data_samples.values()]
all_equal_length = all(length == lengths[0] for length in lengths)

extended_data_samples = []

if all_equal_length:
    for idx, question in enumerate(data_samples['question']):
        model = ChatOpenAI(model="gpt-4", temperature=0.9)

        print("Configuring retriever...")
        retriever = EvalDB.db.as_retriever()
        retriever.search_kwargs['score_threshold'] = 0.8
        retriever.search_kwargs['fetch_k'] = 50
        retriever.search_kwargs['search_type'] = 'mmr'  # todo: make the search_kwargs configurable
        retriever.search_kwargs['lambda_mult'] = '0.7'
        retriever.search_kwargs['k'] = 8
        print("loaded retriever")

        qa = ConversationalRetrievalChain.from_llm(
            llm=model, retriever=retriever, verbose=True)

        answer = qa.run({"question": question, "chat_history": []})

        if not answer:
            print('Is the token present and correct?.')

        else:
            context_df = []
            context = retriever.get_relevant_documents(query=question)

            for con in context:
                con_json = con.to_json()
                page_content = con_json['kwargs']['page_content']
                context_df.append(page_content)

            # Hier context df und answer in data_samples hinzufügen
            extended_data_samples.append({
                'Question': question,
                'Answer': answer,
                'Contexts': context_df,
                'Ground Truth': data_samples['ground_truth'][idx],
            })
else:
    print("Nicht alle Schlüssel haben die gleiche Anzahl von Elementen.")

# Convert the extended_data_samples list of dictionaries into a DataFrame
extended_df = pd.DataFrame(extended_data_samples)

# Save the DataFrame as an Excel file
extended_df.to_excel('testset.xlsx', index=False)
