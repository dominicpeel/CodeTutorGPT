import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd
import ast
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import openai

from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv('embeddings.csv')
embeddings_col = df['embedding']

matrix = np.array(embeddings_col.apply(ast.literal_eval).tolist())

tsne_3d = TSNE(n_components=3, perplexity=15, random_state=42,
               init='random', learning_rate=200)
vis_dims_3d = tsne_3d.fit_transform(matrix)
vis_dims_3d.shape

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x_3d = [x for x, y, z in vis_dims_3d]
y_3d = [y for x, y, z in vis_dims_3d]
z_3d = [z for x, y, z in vis_dims_3d]

unique_docs = df['document'].unique()
colors = plt.cm.get_cmap('viridis', len(unique_docs))
doc_color_map = {doc: colors(idx) for idx, doc in enumerate(unique_docs)}

# Assign colors based on document values
colors_list = df['document'].map(doc_color_map).tolist()

ax.scatter(x_3d, y_3d, z_3d, c=colors_list)

ax.set_title(
    "t-SNE dim reduction")
plt.show()

query = 'a pointer is a variable that stores the address of another variable'

res = openai.Embedding.create(
    input=[query],
    engine='text-embedding-ada-002'
)['data'][0]['embedding']

# Calculate cosine similarity between the query embedding and all embeddings
query_embedding = np.array(res).reshape(1, -1)
cosine_sim = cosine_similarity(query_embedding, matrix)

k = 10 
# Get the indices of the top 10 similar embeddings
top_k_indices = cosine_sim.argsort()[0][-k:][::-1]

# Retrieve the corresponding rows from the DataFrame
top_k_similar_embeddings = df.iloc[top_k_indices]

# print the top embedding
print(top_k_similar_embeddings['document'].iloc[0])
print(top_k_similar_embeddings['text'].iloc[0])

# Modify colors_list to highlight the top 10 similar embeddings
highlight_color = (1, 0, 0, 1)  # RGBA color for the similar embeddings (red in this case)
for idx in top_k_indices:
    colors_list[idx] = highlight_color

# Add the query point to the scatter plot with a unique color and marker style
vis_dims_3d_with_query = tsne_3d.fit_transform(np.vstack([matrix, query_embedding]))

query_x, query_y, query_z = vis_dims_3d_with_query[-1] 
query_color = (0, 1, 0, 1)  # RGBA color for the query point (green in this case)
query_marker = 'X'  # Marker style for the query point

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the original points
ax.scatter(x_3d, y_3d, z_3d, c=colors_list)

# Plot the query point
ax.scatter(query_x, query_y, query_z, c=query_color, marker=query_marker, s=100, edgecolor='black', linewidths=1)

ax.set_title("t-SNE dim reduction with query and similar embeddings highlighted")
plt.show()