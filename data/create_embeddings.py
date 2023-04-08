import pandas as pd
from uuid import uuid4
from time import sleep
from tqdm.auto import tqdm
import openai
import pinecone
import tiktoken
import PyPDF2

from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
model = "text-embedding-ada-002"
dim = 1536  # ada-002 embedding dimension

# get all pdf documents to embed
ls = os.listdir('documents')
files = [f for f in ls if f.endswith('.pdf')]

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

tokenizer = tiktoken.get_encoding('p50k_base')

# create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

# split text into ~400 token chunks
def text_splitter(text, chunk_size=400, separators=['\n\n', '\n', ' ', '']):
    def find_optimal_separator(text):
        for sep in separators:
            chunks = text.split(sep)
            if all(tiktoken_len(chunk) <= chunk_size for chunk in chunks):
                return sep
        return ''

    chunks = []
    optimal_separator = find_optimal_separator(text)
    split_text = text.split(optimal_separator)

    current_chunk = ''
    current_chunk_token_count = 0

    for part in tqdm(split_text):
        part_token_count = tiktoken_len(part)

        if current_chunk_token_count + part_token_count + tiktoken_len(optimal_separator) <= chunk_size:
            current_chunk += (optimal_separator + part)
            current_chunk_token_count += part_token_count
        else:
            chunks.append(current_chunk.strip())
            current_chunk = part
            current_chunk_token_count = part_token_count

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


chunks = []
print('splitting text into 400 token chunks...')
for f in files:
    print(f)
    text = extract_text_from_pdf(f'documents/{f}')
    texts = text_splitter(text)
    chunks.extend([{
        'id': str(uuid4()),
        'document': f,
        'text': texts[i],
        'chunk': i,
    } for i in range(len(texts))])

print('total chunks:', len(chunks))

# create the embeddings
columns = ['chunk', 'id', 'document', 'text', 'embedding']
df = pd.DataFrame(columns=columns)

print('creating embeddings...')
for chunk in tqdm(chunks):
    res = openai.Embedding.create(
        input=[chunk['text']],
        engine=model
    )
    chunk['embedding'] = res['data'][0]['embedding']

    # Create a temporary DataFrame to store the current chunk data
    temp_df = pd.DataFrame([chunk], columns=columns)
    
    # Concatenate the temporary DataFrame with the main DataFrame
    df = pd.concat([df, temp_df], ignore_index=True)

df.to_csv('embeddings.csv', index=False)
