import json
import torch
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# === CONFIG ===
MODEL_PATH = r"TU WPISZ ŚCIEŻKĘ DO MODELU EMBEDDUJĄCEGO"
JSONL_PATH = "frazy_kredyt_hipoteczny.jsonl"
OUTPUT_JSON = "frazy_wyniki.json"

# === LOAD MODEL ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModel.from_pretrained(MODEL_PATH)

def embed_text(text):
    tokens = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        output = model(**tokens)
    embedding = output.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# === LOAD QUERIES ===
queries = []
with open(JSONL_PATH, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        queries.append(obj["query"])

# === GENERATE EMBEDDINGS ===
embeddings = []
for q in tqdm(queries, desc="Embedding"):
    embeddings.append(embed_text(q))

embeddings = np.array(embeddings)

# === COMPUTE CENTROID & DISTANCES ===
centroid = np.mean(embeddings, axis=0)
cos_sim = lambda a, b: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
distances = [1 - cos_sim(vec, centroid) for vec in embeddings]

# === CLASSIFY INTO CATEGORIES ===
categories = []
for d in distances:
    if d < 0.25:
        categories.append("core")
    elif d < 0.45:
        categories.append("semi")
    else:
        categories.append("drift")

# === PCA TO 2D ===
pca = PCA(n_components=2)
coords_2d = pca.fit_transform(embeddings)

# === SAVE TO JSON ===
results = []
for q, d, cat, coords in zip(queries, distances, categories, coords_2d):
    results.append({
        "query": q,
        "distance_from_centroid": round(float(d), 4),
        "class": cat,
        "x": round(float(coords[0]), 4),
        "y": round(float(coords[1]), 4)
    })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Zapisano wyniki do: {OUTPUT_JSON}")

# === PLOT ===
plt.figure(figsize=(10, 7))
colors = {"core": "green", "semi": "orange", "drift": "red"}
color_values = [colors[c] for c in categories]

plt.scatter(coords_2d[:, 0], coords_2d[:, 1], c=color_values, s=10, alpha=0.7)

plt.title("Rozrzut semantyczny")
legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=k, markersize=8, markerfacecolor=v) for k, v in colors.items()]
plt.legend(handles=legend_labels, title="Kategoria")
plt.tight_layout()
plt.show()
