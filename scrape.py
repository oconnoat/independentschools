import time
import requests

for page in range(1,70):
    time.sleep(1)
    with open(('html/page%s.html' % page), 'w') as thefile:
        print page
        thefile.write(requests.get('http://education.independent.ie/league',
            params={'page':page}).content)
