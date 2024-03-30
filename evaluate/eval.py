from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate
from ragas.metrics import faithfulness, answer_correctness
import pandas as pd
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
df = pd.read_excel('testset.xlsx')

# Create the 'data_samples' dictionary structure
data_samples = {
    'question': df['Question'].tolist(),
    'answer': df['Answer'].tolist(),
    'contexts': df['Contexts'].apply(lambda x: [x] if pd.notna(x) else []).tolist(),
    'ground_truth': df['Ground Truth'].tolist()
}

print(data_samples['answer'])

dataset = Dataset.from_dict(data_samples)
score = evaluate(dataset,metrics=[faithfulness,answer_correctness])
print(score)