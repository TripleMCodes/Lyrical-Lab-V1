from embeddings import SentenceTransformerProvider

emb = SentenceTransformerProvider()
v = emb.embed(["midnight echoes in my head"])
print(v.shape)
