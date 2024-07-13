import orjson
from collections import Counter
from typing import List, Tuple

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON para encontrar los 10 usuarios 
    más mencionados y su cantidad de menciones.

    Esta función está optimizada para un uso eficiente de la memoria.
    Args:
        file_path (str): Ruta al archivo que contiene los datos de los tweets.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas donde cada tupla contiene 
                               un usuario y su cantidad de menciones.
    """
    mention_count = Counter()

    def process_tweet(tweet):
        mentioned_users = tweet.get('mentionedUsers', [])
        if mentioned_users:
            usernames = [user['username'] for user in mentioned_users if user]
            mention_count.update(usernames)

    with open(file_path, 'rb') as file:
        for line in file:
            tweet = orjson.loads(line)
            process_tweet(tweet)

    top_10_users = mention_count.most_common(10)

    return top_10_users