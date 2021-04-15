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

search_link = engine_url + search_link_ilibrary(name.upper()) #Getting a full link for our search request

print(search_link)

session = requests.get(search_link, headers=HEADERS) #Session for the requests
soup = BeautifulSoup(session.text, 'lxml')

try: #Trying to get the result of search
    amount_of_books = soup.find('span', attrs={'style': 'font-size: 75%; color: #666666;'}).find('b') #Find amount of books or authors it has found
except:
    amount_of_books = 0
    print("Found Books or Authors: " + str(amount_of_books))
    print("Try again!")
    exit()

print("Found Books or Authors: " + amount_of_books.text)
if (amount_of_books.text != "0"): #Ask for countinue
    des = ''
    while (des != 'n' or des != 'N' or des != 'Y' or des != 'y'):
        print("Open the following book or author biography?: Y/N")
        des = input()
        if(des == 'N' or des == 'n'):
            exit()
        elif(des == 'Y' or des == 'y'):
            break
else:
    print("No books or authors with this name")

text_link = 'https://ilibrary.ru' + str(soup.find('li').find('a').get('href')) #Getting link for the text of book or biography
print(text_link)

    


