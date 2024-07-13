import numpy as np
import orjson
from typing import List, Tuple
from datetime import datetime, date, timedelta
import mmap

def q1_time(file_path: str) -> List[Tuple[date, str]]:
    """
    Procesa un archivo de tweets en formato JSON para encontrar las 10 fechas
    con más tweets y el usuario con más tweets en cada una de esas fechas.

    Esta función esta optimizada para por tiempo de ejecución mediante el uso
    de numpy para la creación de un arreglo de ceros y la función argsort para
    encontrar los índices de las fechas con más tweets.

    Args:
        file_path (str): Ruta al archivo que contiene los datos de los tweets.

    Returns:
        List[Tuple[date, str]]: Una lista de tuplas donde cada tupla contiene 
                                una fecha y el nombre de usuario con más tweets en esa fecha.
    """
    # Assume the date range (adjust as needed)
    start_date = date(2020, 1, 1)
    end_date = date(2023, 12, 31)
    date_range = (end_date - start_date).days + 1

    # Pre-allocate arrays
    tweet_counts = np.zeros(date_range, dtype=np.int32)
    user_counts = {}

    def process_tweet(tweet_date, username):
        day_index = (tweet_date - start_date).days
        tweet_counts[day_index] += 1
        if day_index not in user_counts:
            user_counts[day_index] = {}
        user_counts[day_index][username] = user_counts[day_index].get(username, 0) + 1

    with open(file_path, 'rb') as file:
        mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(mmapped_file.readline, b''):
            tweet = orjson.loads(line)
            tweet_date = datetime.strptime(tweet['date'][:10], '%Y-%m-%d').date()
            username = tweet['user']['username']
            process_tweet(tweet_date, username)

    top_10_indices = np.argsort(tweet_counts)[-10:][::-1]
    
    result = []
    for idx in top_10_indices:
        top_date = start_date + timedelta(days=int(idx))
        if idx in user_counts:
            top_user = max(user_counts[idx].items(), key=lambda x: x[1])[0]
        else:
            top_user = "Unknown"  # Handle case where no user data is available
        result.append((top_date, top_user))

    return result
