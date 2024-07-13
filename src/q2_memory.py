import datetime
import orjson
from collections import Counter
from typing import List, Tuple
import re


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON para encontrar los 10 emojis
    más usados y su cantidad de usos.

    Esta función está optimizada para un uso eficiente de la memoria.
    Args:
        file_path (str): Ruta al archivo que contiene los datos de los tweets.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas donde cada tupla contiene 
                               un emoji y su cantidad de usos.
    """
    emoji_count = Counter()
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)


    def process_tweet(tweet):
        text = tweet['renderedContent']
        emojis = emoji_pattern.findall(text)
        emoji_count.update(emojis)
   
    with open(file_path, 'rb') as file:
        for line in file:
            tweet = orjson.loads(line)
            process_tweet(tweet)
   
    top_10_emojis = emoji_count.most_common(10)
   
    return top_10_emojis