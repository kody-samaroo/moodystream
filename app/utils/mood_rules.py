# app/utilts/mood_rules.py

def classify_mood(features):
    if not features:
        return "unknown"

    valence = features['valence']
    energy = features['energy']

    if valence > 0.7 and energy > 0.7:
        return "happy"
    elif valence < 0.4 and energy < 0.4:
        return "sad"
    elif energy > 0.7:
        return "energetic"
    elif valence > 0.7:
        return "chill"
    else:
        return "neutral"
