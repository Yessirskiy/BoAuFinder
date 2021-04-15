import requests
import urllib.parse 
from bs4 import BeautifulSoup

def search_link_ilibrary(name): #make an addition to the ilibrary search link using ascii codes
    name_url = ""
    for letter in name:
        #print(ord(letter))
        if ((ord(letter) < 1040 or ord(letter) > 1103) and ord(letter) != 32):
            print("Non russian letter")
        else:
            if ord(letter) == 32:
                name_url += '+'
            elif (ord(letter) <= 1055):
                name_url += '%'
                name_url += 'C'
                if (ord(letter) <= 1049):
                    name_url += str(ord(letter)%10)
                else:
                    name_url += chr(ord(letter) - 985)
            elif (ord(letter) <= 1071):
                name_url += '%'
                name_url += 'D'
                if (ord(letter) <= 1065):
                    name_url += str((ord(letter) - 6)%10)
                else:
                    name_url += chr(ord(letter) - 1001)
    return name_url


engine_url = 'https://ilibrary.ru/search.phtml?q=' #Site with online books - ilibrary

HEADERS = { #Headers for site requests
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }

print("Type name of the book or author: ")
name = input() #Getting name of the book or author

search = engine_url + search_link_ilibrary(name.upper()) #Getting a full link for our search request

print(search)
