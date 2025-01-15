LANGUAGE_CODES = {
    "english": "eng_Latn",
    "french": "fra_Latn",
    "spanish": "spa_Latn",
    "german": "deu_Latn",
    "italian": "ita_Latn",
    "portuguese": "por_Latn",
    "arabic": "arb_Arab",
    "hindi": "hin_Deva",
    "chinese": "zho_Hans",
    "russian": "rus_Cyrl",
}

language_name = input("Enter the target language (e.g., 'french', 'spanish', 'arabic'): ").lower()
target_language = LANGUAGE_CODES.get(language_name)

print(target_language)

if not target_language:
    print("Invalid language. Please try again.")
    exit()
