# Exploring Word Embeddings in AI: A Visual Journey with Heatmaps

- get_embedding function is used to get the embedding of a word form OpenAI Embedding.
- compare_embeddings function is used to compare the embeddings of two words. It uses cache (compare_cache.json) to store the embeddings of the words locally to avoid API calls


**Note:**
- np.nan if score < 2.75e-06 else score is used to avoid the heatmap to be dominated by the very low values.