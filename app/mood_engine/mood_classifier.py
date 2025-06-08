# moodystream/mood_engine/mood_classifier.py

def classify_mood(audio_features):
    energy = audio_features.get('energy', 0)
    valence = audio_features.get('valence', 0)
    tempo = audio_features.get('tempo', 0)
    danceability = audio_features.get('danceability', 0)
    acousticness = audio_features.get('acousticness', 0)

    if energy < 0.4 and valence < 0.5 and acousticness > 0.5:
        return "Chill"
    elif energy > 0.7 and danceability > 0.6 and valence > 0.4:
        return "Energetic"
    elif valence < 0.4 and energy < 0.5:
        return "Melancholy"
    elif valence > 0.6 and 0.5 < energy < 0.7 and tempo > 100:
        return "Upbeat"
    else:
        return "Uncategorized"
