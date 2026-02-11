from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

LYRIC_STOPWORDS = {
    "yeah", "yea", "yuh", "uh", "uhh", "oh", "ooh", "woo", "woah",
    "ayy", "ay", "aight", "nah", "huh", "mm", "mmm",
    "la", "na", "doo", "da","baby", "babe",
}

DEFAULT_STOPWORDS = set(ENLISH_STOP_WORDS) | LYRIC_STOPWORDS