from typing import List, Tuple
import datetime
import json
from collections import defaultdict, Counter

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Step 1: Initialize counters
    date_tweet_count = Counter()
    date_user_count = defaultdict(Counter)
    
    # Step 2: Read and process the file line-by-line
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line.strip())
            
            date_str = tweet['date'][:10]
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            username = tweet['user']['username']
            
            date_tweet_count[date] += 1
            date_user_count[date][username] += 1
    
    # Step 3: Find the top 10 dates with the most tweets
    top_10_dates = date_tweet_count.most_common(10)
    
    # Step 4: Find the user with the most publications for each top date
    result = []
    for date, _ in top_10_dates:
        top_user = date_user_count[date].most_common(1)[0][0]
        result.append((date, top_user))
    
    return result
