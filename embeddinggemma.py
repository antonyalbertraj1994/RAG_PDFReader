# import os
# print("Anto122")
#
# from sentence_transformers import SentenceTransformer
# # from huggingface_hub import InferenceClient
# #
# # client = InferenceClient(
# #     provider="hf-inference",
# #     api_key=os.environ["HF_TOKEN"],
# # )
# # Download from the 🤗 Hub
# print("Anto12")
#
# model = SentenceTransformer("google/embeddinggemma-300m")
# print("Anto")
#
# # Run inference with queries and documents
# query = "Which planet is known as the Red Planet?"
# documents = [
#     "Venus is often called Earth's twin because of its similar size and proximity.",
#     "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
#     "Jupiter, the largest planet in our solar system, has a prominent red spot.",
#     "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
# ]
# query_embeddings = model.encode_query(query)
# print("dfsd")
# document_embeddings = model.encode_document(documents)
# print("dfsd123")
#
# print(query_embeddings.shape, document_embeddings.shape)
# # (768,) (4, 768)
#
# # Compute similarities to determine a ranking
# similarities = model.similarity(query_embeddings, document_embeddings)
# print(similarities)



import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b:groq",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],1
)

print(completion.choices[0].message)