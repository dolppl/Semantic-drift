# Semantic Drift – analiza rozrzutu semantycznego fraz kluczowych

Ten projekt pokazuje, jak zmierzyć **rozrzut semantyczny fraz** wygenerowanych z Google Suggest, na przykładzie hasła „kredyt hipoteczny”.

Wizualizacja pozwala zrozumieć, które zapytania są blisko głównego tematu (core), a które zaczynają **dryfować semantycznie** (drift), co jest szczególnie przydatne w SEO, NLP i analizie intencji użytkowników.

---

## Co robi ten projekt

1. Wczytuje frazy z pliku `.jsonl` (z Google Autocomplete)
2. Generuje embeddingi fraz lokalnym modelem 
3. Oblicza odległość każdej frazy od centroidu (średniego embeddingu)
4. Dzieli frazy na:
   - `core` – bardzo zbliżone do głównego tematu
   - `semi` – poboczne
   - `drift` – semantycznie odklejone
5. Tworzy wykres PCA w 2D

---

## ⚙Jak uruchomić

Zainstaluj zależności:

pip install -r requirements.txt
