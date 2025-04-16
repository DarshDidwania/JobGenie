import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from db import fetch_jobs

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def prepare_data():
    jobs = fetch_jobs()
    df = pd.DataFrame(jobs)
    df['full_text'] = df['jtitle'].fillna('') + " " + df['jdescription'].fillna('') + " " + df['jkeywords'].fillna('')
    df['embedding'] = df['full_text'].apply(lambda x: model.encode(x, convert_to_tensor=True))
    return df

def match_jobs(query, df, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = [util.pytorch_cos_sim(query_embedding, emb).item() for emb in df['embedding']]
    df['score'] = scores
    return df.sort_values('score', ascending=False).head(top_k)
