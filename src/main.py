import requests
import random
import time
import json

quizzes_type = 2

base_url = 'https://quizizz.com/_api/main'

quizzes_url = base_url + f'/adminRecommend/{quizzes_type}'

#endpoint = 'https://quizizz.com/_api/main/v2/adminRecommend/2?page=3&pageSize=12'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/58.0.3029.110 Safari/537.3'
}

max_retries = 5
retry_delay = 1
retry_count = 0

quizzes_list = []

for i in range(1, 2):
    try:
        response = requests.get(f'{quizzes_url}?page={i}&pageSize={12}', headers = headers)
        
        if response.status_code == 200:
            
            response_data = response.json()
            
            quizzes_data = response_data['data']['quizzes']
            
            for quiz in quizzes_data:
                quiz_info = {
                    'name': quiz['info']['name']
                }
                
                quizzes_list.append(quiz_info)
                #print(quiz_info)
            
            #break
        elif response.status_code == 429:
            
            print(f"Rate limited. Retrying in {retry_delay} seconds...")
            
            time.sleep(retry_delay)
            
            retry_delay *= 2
            
            retry_count += 1
            
            if retry_count >= max_retries:
                break
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        print(e)
    
    sleep_time = random.randint(1, 10)
    
    print(f"Sleeping for {sleep_time} seconds...")
    
    time.sleep(sleep_time)
    
with open('./data/quizzes.json', 'w', encoding = 'utf-8') as f:
    json.dump(quizzes_list, f, ensure_ascii = False, indent = 4)    
    
#print(quizzes_list)