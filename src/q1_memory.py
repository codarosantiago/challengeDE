import datetime
import orjson
from collections import Counter
from typing import List, Tuple

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Procesa un archivo de tweets en formato JSON para encontrar las 10 fechas
    con más tweets y el usuario con más tweets en cada una de esas fechas.

    La función esta optimizada para ser eficiente en el uso de la memoria.

    Args:
        file_path (str): Ruta al archivo que contiene los datos de los tweets.

    Returns:
        List[Tuple[datetime.date, str]]: Una lista de tuplas donde cada tupla contiene 
                                         una fecha y el nombre de usuario con más tweets en esa fecha.
    """
    date_tweet_count = Counter()
    date_user_count = {}
    
    def process_tweet(tweet):
        date = datetime.datetime.strptime(tweet['date'][:10], '%Y-%m-%d').date()
        username = tweet['user']['username']
        
        date_tweet_count[date] += 1
        if date not in date_user_count:
            date_user_count[date] = Counter()
        date_user_count[date][username] += 1
    
    with open(file_path, 'rb') as file:
        for line in file:
            tweet = orjson.loads(line)
            process_tweet(tweet)
    
    top_10_dates = date_tweet_count.most_common(10)
    
    result = [
        (date, date_user_count[date].most_common(1)[0][0])
        for date, _ in top_10_dates
    ]
    
    return result