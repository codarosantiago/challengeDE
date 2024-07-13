import numpy as np
import orjson
from typing import List, Tuple
from datetime import datetime
import mmap
import re

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON para encontrar los 10 emojis
    más usados y su cantidad de usos.

    Esta función está optimizada por tiempo de ejecución mediante el uso de 
    mmap para la lectura eficiente del archivo y expresiones regulares para 
    la extracción de emojis.

    Args:
        file_path (str): Ruta al archivo que contiene los datos de los tweets.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas donde cada tupla contiene 
                               un emoji y su cantidad de usos.
    """
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U00002300-\U000023FF"  # Miscellaneous Technical
        "]+", flags=re.UNICODE
    )

    emoji_counts = {}

    def process_tweet(tweet_text):
        emojis = emoji_pattern.findall(tweet_text)
        for emoji in emojis:
            if emoji in emoji_counts:
                emoji_counts[emoji] += 1
            else:
                emoji_counts[emoji] = 1

    with open(file_path, 'rb') as file:
        mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(mmapped_file.readline, b''):
            tweet = orjson.loads(line)
            tweet_text = tweet['renderedContent']
            process_tweet(tweet_text)

    top_10_emojis = sorted(emoji_counts.items(), key=lambda item: item[1], reverse=True)[:10]

    return top_10_emojis