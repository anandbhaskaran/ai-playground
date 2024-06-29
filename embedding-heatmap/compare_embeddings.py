from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import load_evaluator
from dotenv import load_dotenv
import openai
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


# Cache the compare function in a file
def cache_compare():
    if os.path.exists("compare_cache.json"):
        with open("compare_cache.json", "r") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open("compare_cache.json", "w") as f:
        json.dump(cache, f)


def compare_embeddings(word1, word2):
    cache = cache_compare()
    key = f"{word1}+{word2}"
    if key in cache:
        return cache[key]
    evaluator = load_evaluator("pairwise_embedding_distance")
    x = evaluator.evaluate_string_pairs(prediction=word1, prediction_b=word2)
    print(f"New: Comparing {word1} and {word2}: {x['score']}")
    cache[key] = x['score']
    save_cache(cache)
    return x['score']


# Get embedding-heatmap for a word.
def get_embedding(word):
    embedding_function = OpenAIEmbeddings()
    vector = embedding_function.embed_query(word)
    print(f"Vector for {word}: {vector}")
    print(f"Vector length: {len(vector)}")

if __name__ == "__main__":
    # Get the embeddings for a word
    get_embedding("apple")

    # List of words to compare
    words_list = ["apple", "iphone", "orange", "windows", "microsoft", "bat",
                  "baseball", "animal", "mouse", "computer"]

    # Create a list of scores for each word pair
    scores = []
    for word in words_list:
        row = []
        for word2 in words_list:
            score = compare_embeddings(word, word2)
            row.append(np.nan if score < 2.75e-06 else score)
        scores.append(row)

    # Convert the scores list to a numpy array
    data = np.array(scores)


    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(data, xticklabels=words_list, yticklabels=words_list, annot=True, fmt=".2f", cmap='RdYlGn_r', ax=ax)
    ## Make title font size larger
    plt.title("Word Embedding Similarity Heatmap", fontsize=20, pad=40, loc='right')
    plt.savefig('heatmap.png')
    plt.show()
