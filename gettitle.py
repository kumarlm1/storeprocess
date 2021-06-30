import urllib.request
import json
import urllib
import pprint

#change to yours VideoID or change url inparams
VideoID = "Ocj0sVB9ykY" 

params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
url = "https://www.youtube.com/oembed"
query_string = urllib.parse.urlencode(params)
url = url + "?" + query_string
print(url)
with urllib.request.urlopen(url) as response:
    response_text = response.read()
    data = json.loads(response_text.decode())
    print(data['title'])