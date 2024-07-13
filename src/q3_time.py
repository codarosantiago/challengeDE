import mmap
import orjson
from typing import List, Tuple

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON para encontrar los 10 usuarios
    más mencionados y su cantidad de menciones.

    Esta función está optimizada por tiempo de ejecución mediante el uso de 
    mmap para la lectura eficiente del archivo.

    Args:
        file_path (str): Ruta al archivo que contiene los datos de los tweets.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas donde cada tupla contiene 
                               un nombre de usuario y su cantidad de menciones.
    """
    user_mention_counts = {}

    def process_tweet(tweet):
        mentioned_users = tweet.get('mentionedUsers')
        if mentioned_users:
            for user in mentioned_users:
                username = user['username']
                if username in user_mention_counts:
                    user_mention_counts[username] += 1
                else:
                    user_mention_counts[username] = 1

    with open(file_path, 'rb') as file:
        mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(mmapped_file.readline, b''):
            tweet = orjson.loads(line)
            process_tweet(tweet)

    top_10_users = sorted(user_mention_counts.items(), key=lambda item: item[1], reverse=True)[:10]

    return top_10_users
