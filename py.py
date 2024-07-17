import http.client

conn = http.client.HTTPSConnection("ott-details.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "bbcfdac50amsh60af14119911f66p18ab9fjsn77a641adfe85",
    'x-rapidapi-host': "ott-details.p.rapidapi.com"
}

conn.request("GET", "/getParams?param=genre", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))