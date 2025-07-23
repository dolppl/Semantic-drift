import requests
import time
import string

def get_google_suggest(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    response = requests.get(url).json()
    return response[1] if len(response) > 1 else [] 

def expand_suggestions(base_keyword):
    all_suggestions = set()
    
    print(f"Pobieranie sugestii dla: {base_keyword}")
    
    suggestions = get_google_suggest(base_keyword)
    all_suggestions.update(suggestions)
    
    for letter in string.ascii_lowercase + " ąćęłńóśźż":
        new_keyword = f"{base_keyword} {letter}"
        print(f"Sprawdzam: {new_keyword}...")
        suggestions = get_google_suggest(new_keyword)
        all_suggestions.update(suggestions)
        time.sleep(0.5)
    
    for letter1 in string.ascii_lowercase:
        for letter2 in string.ascii_lowercase:
            new_keyword = f"{base_keyword} {letter1}{letter2}"
            print(f"Sprawdzam: {new_keyword}...")
            suggestions = get_google_suggest(new_keyword)
            all_suggestions.update(suggestions)
            time.sleep(0.5)
    
    question_words = ["jak", "ile", "gdzie", "czy", "co", "kiedy", "dlaczego"]
    
    for word in question_words:
        new_keyword = f"{word} {base_keyword}"
        print(f"Sprawdzam: {new_keyword}...")
        suggestions = get_google_suggest(new_keyword)
        all_suggestions.update(suggestions)
        time.sleep(0.5)
        
        for letter in string.ascii_lowercase:
            new_question_keyword = f"{new_keyword} {letter}"
            print(f"Sprawdzam: {new_question_keyword}...")
            suggestions = get_google_suggest(new_question_keyword)
            all_suggestions.update(suggestions)
            time.sleep(0.5)
        
        for letter1 in string.ascii_lowercase:
            for letter2 in string.ascii_lowercase:
                new_question_keyword = f"{new_keyword} {letter1}{letter2}"
                print(f"Sprawdzam: {new_question_keyword}...")
                suggestions = get_google_suggest(new_question_keyword)
                all_suggestions.update(suggestions)
                time.sleep(0.5)
    
    print(f"Łącznie zebrano: {len(all_suggestions)} unikalnych fraz")
    return list(all_suggestions)

keyword = "kredyt hipoteczny"
expanded_results = expand_suggestions(keyword)

filename = "frazy.txt"
with open(filename, "w", encoding="utf-8") as file:
    for result in expanded_results:
        file.write(result + "\n")

print(f"\n Wszystkie frazy zapisano do: {filename}")
