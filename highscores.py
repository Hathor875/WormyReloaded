import yaml
import os
from datetime import datetime

HIGHSCORE_FILES = {
    "Portal Mode": "highscores_portal.yml",
    "Wall Death": "highscores_wall.yml"
}

DEFAULT_SCORES = {
    "Portal Mode": [
        {"score": 1000, "name": "MSTR", "difficulty": "HARD", "date": "2025-06-19 12:00"},
        {"score": 800, "name": "PRO1", "difficulty": "MID", "date": "2025-06-19 12:00"},
        {"score": 500, "name": "ROOK", "difficulty": "EASY", "date": "2025-06-19 12:00"}
    ],
    "Wall Death": [
        {"score": 750, "name": "EXPR", "difficulty": "HARD", "date": "2025-06-19 12:00"},
        {"score": 600, "name": "SKLD", "difficulty": "MID", "date": "2025-06-19 12:00"},
        {"score": 400, "name": "BEGN", "difficulty": "EASY", "date": "2025-06-19 12:00"}
    ]
}

# Inicjalizacja pliku dla danego trybu
def init_highscore_file(mode):
    file = HIGHSCORE_FILES[mode]
    if not os.path.exists(file):
        with open(file, 'w') as f:
            yaml.dump(DEFAULT_SCORES[mode], f)

# Odczyt rekordów dla danego trybu
def read_highscores(mode):
    init_highscore_file(mode)
    file = HIGHSCORE_FILES[mode]
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
            # Upewnij się, że dane są listą i wszystkie wyniki są liczbami
            if not isinstance(data, list):
                data = []
            # Usuń wpisy z nieprawidłowymi wynikami
            data = [entry for entry in data if isinstance(entry, dict) and 
                   isinstance(entry.get('score'), (int, float))]
    except:
        data = []
    return data if data else DEFAULT_SCORES[mode]

# Zapis nowego rekordu (tylko jeśli mieści się w top 10)
def save_highscore(mode, score, name, difficulty):
    if not isinstance(score, (int, float)):
        return None  # Ignoruj nieprawidłowe wyniki
    
    init_highscore_file(mode)
    file = HIGHSCORE_FILES[mode]
    data = read_highscores(mode)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Upewnij się, że name ma dokładnie 4 znaki
    name = name[:4].upper()
    if len(name) < 4:
        name = name.ljust(4, '_')
    
    new_entry = {
        "score": int(score),
        "name": name,
        "difficulty": difficulty,
        "date": now
    }
    
    data.append(new_entry)
    # Sortuj malejąco i zostaw tylko 10 najlepszych
    data = sorted(data, key=lambda x: int(x['score']), reverse=True)[:10]
    
    try:
        with open(file, 'w') as f:
            yaml.dump(data, f)
    except Exception as e:
        print(f"Error saving highscore: {e}")
        return None
    
    return data
