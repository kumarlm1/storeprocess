import requests
import urllib.parse

# you can modify size, format, zoom
BASE = 'https://mini.s-shot.ru/1024x0/JPEG/1024/Z100/?'
url = 'https://stackoverflow.com/'  # or whatever link you need
url1 ="https://datacadamia.com/ide/notepad/replace#take_all_letters_until_a_separator_character_is_reached"
# service needs link to be joined in encoded format
url = urllib.parse.quote_plus(url1)
print(url)

path = 'target1.jpg'
response = requests.get(BASE + url, stream=True)

if response.status_code == 200:
    with open(path, 'wb') as file:
        for chunk in response:
            file.write(chunk)
print('finished')