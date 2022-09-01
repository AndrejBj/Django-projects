from urllib import response
import requests                            #biblioteka koja omogucava slanje HTTP requests
import json

response=requests.get("https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow")

#print(response.json())                    #vraca nam source kod iz linka iznad
#print(response.json()["items"])           #uneli smo kljuc items za koji cemo kao ispis dobiti vrednosti
for data in response.json()["items"]:      #za kljuc items
    print(data["title"])                   #kupimo samo title kljuceve i vrednosti unutar njih (znaci kljuc unutar kljuca)

print("----------")
for data in response.json()["items"]:     
    if(data["answer_count"]==0):
        print(data["title"])
        print(data["link"])
        print()
    else:
        print("skipped")
    print()