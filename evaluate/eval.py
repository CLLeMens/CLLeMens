from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate
from ragas.metrics import faithfulness, answer_correctness, context_precision, answer_relevancy, context_recall
import pandas as pd
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
df = pd.read_excel('testset.xlsx')

# Create the 'data_samples' dictionary structure
data_samples = {
    'question': df['Question'].tolist(),
    'answer': df['Answer'].tolist(),
    'contexts': df['Context'].apply(lambda x: [x] if pd.notna(x) else []).tolist(),
    'ground_truth': df['Ground Truth'].tolist()
}

dataset = Dataset.from_dict(data_samples)
score = evaluate(
    dataset,
    metrics=[
        context_precision,
        faithfulness,
        answer_correctness,
        answer_relevancy,
        context_recall,
    ],
)
print(score)
