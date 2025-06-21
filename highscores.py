import yaml
import os


HIGHSCORE_FILES = {
    "Portal Mode": "highscores_portal.yml",
    "Wall Death": "highscores_wall.yml"
}

DEFAULT_SCORES = {
    "Portal Mode": [
        {"score": 1000, "name": "MSTR"},
        {"score": 800, "name": "PRO1"},
        {"score": 500, "name": "ROOK"}
    ],
    "Wall Death": [
        {"score": 750, "name": "EXPR"},
        {"score": 600, "name": "SKLD"},
        {"score": 400, "name": "BEGN"}
    ]
}


def init_highscore_file(mode):
    file = HIGHSCORE_FILES[mode]
    if not os.path.exists(file):
        with open(file, 'w') as f:
            yaml.dump(DEFAULT_SCORES[mode], f)


def read_highscores(mode):
    init_highscore_file(mode)
    file = HIGHSCORE_FILES[mode]
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
            if not isinstance(data, list):
                data = []
            data = [entry for entry in data if isinstance(entry, dict) and 
                   isinstance(entry.get('score'), (int, float))]
    except:
        data = []
    return data if data else DEFAULT_SCORES[mode]


def save_highscore(mode, score, name, difficulty=None):
    if not isinstance(score, (int, float)):
        return None
    
    init_highscore_file(mode)
    file = HIGHSCORE_FILES[mode]
    data = read_highscores(mode)

    name = name[:4].upper()
    if len(name) < 4:
        name = name.ljust(4, '_')
    
    new_entry = {
        "score": int(score),
        "name": name
    }
    
    data.append(new_entry)
    data = sorted(data, key=lambda x: int(x['score']), reverse=True)[:10]
    
    try:
        with open(file, 'w') as f:
            yaml.dump(data, f)
    except Exception as e:
        print(f"Error saving highscore: {e}")
        return None
    
    return data
