import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse

def shorten_link(token, url):
    params = {
        "v": "5.199",
        "url": url,
        "access_token": token,
    }
    
    url_api = 'https://api.vk.com/method/utils.getShortLink'

    response = requests.get(url_api, params=params)
    response.raise_for_status()
    api_response = response.json()  
    short_link = api_response['response']['short_url']
    return short_link


def count_clicks(token, url_path):
    params = {
        "v": "5.199",
        "key": url_path,
        "access_token": token,
        "interval": "forever",
        "extended": "0",
    }
    
    url_api = 'https://api.vk.com/method/utils.getLinkStats'

    response = requests.get(url_api, params=params)
    response.raise_for_status()
    api_response = response.json()
    click_count = api_response['response']['stats'][0]['views']
    return click_count       


def is_shorten_link(token, url):
    url_path = urlparse(url).path.lstrip('/')
    
    params = {
        "v": "5.199",
        "key": url_path,
        "access_token": token,
                }
    
    url_api = 'https://api.vk.com/method/utils.getLinkStats'

    response = requests.get(url_api, params=params)
    response.raise_for_status()
    api_response = response.json()
    return 'error' not in api_response


def main():
    load_dotenv()
    token = os.environ["VK_TOKEN"]
    
    parser = argparse.ArgumentParser(description='Сокращение ссылок и подсчёт переходов по ним.')
    parser.add_argument('url', type=str, help='URL для сокращения или анализа статистики.')
    
    args = parser.parse_args()
    user_input = args.url
    
    try:
        is_short_link = is_shorten_link(token, user_input)

        if is_short_link:
            parsed_url = urlparse(user_input)
            url_path = parsed_url.path.lstrip('/')
            clicks_count = count_clicks(token, url_path)
            print(f"По ссылке перешли: {clicks_count} раз.")
        else:
            short_url = shorten_link(token, user_input)
            print(f"Сокращённая ссылка: {short_url}")
    except requests.exceptions.HTTPError:
        print("Ты по моему перепутал, проверь ссылку!")
    except KeyError:
        print("Ты по моему перепутал, проверь ссылку!")
        

if __name__ == '__main__':
    main()