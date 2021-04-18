import requests
from bs4 import BeautifulSoup
import sys
from docx import Document

def transliterate(name):
   #Dictionary
   dictionary = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'YO',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CH','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'Y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
        
   # Циклически заменяем все буквы в строке
   for key in dictionary:
      name = name.replace(key, dictionary[key])
   return name
def search_link_ilibrary(name): #make an addition to the ilibrary search link using ascii codes
    name_url = ""
    for letter in name:
        if ((ord(letter) < 1040 or ord(letter) > 1103) and ord(letter) != 32 and ord(letter) != 45):
            print("Non russian letter")
        else:
            if ord(letter) == 45:
                name_url += '-'
            elif ord(letter) == 32:
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
def writing_with_spaces(str, file):
    for letter in str:
        if letter == str[-1]:
            file.write(letter)
        else:
            file.write(letter + " ")


engine_url = 'https://ilibrary.ru/search.phtml?q=' #Site with online books - ilibrary

HEADERS = { #Headers for site requests
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }

print("Type name of the book or author: ")
name = input() #Getting name of the book or author

search_link = engine_url + search_link_ilibrary(name.upper()) #Getting a full link for our search request

#print(search_link)

session = requests.get(search_link, headers=HEADERS) #Session for the requests
soup = BeautifulSoup(session.text, 'lxml')

try:
    soup_type = soup.find('span', attrs={'style': 'font-size: 75%; color: #666666;'}) #Check if its authour or book
    if "Найдено авторов:" in soup_type.text:
        #print("This is author")
        type = "authors"
    else:
        #print("This is book")
        type = "books"
except:
    type = "anything"

try: #Trying to get the result of search
    amount_of_type = soup.find('span', attrs={'style': 'font-size: 75%; color: #666666;'}).find('b') #Find amount of books or authors it has found
except:
    amount_of_type = 0
    print("Found " + type + ": " + str(amount_of_type))
    print("Try again!")
    exit()

if (amount_of_type.text != "0"): #Ask for countinue
    des = ''
    while (des != 'n' or des != 'N' or des != 'Y' or des != 'y'):
        print("Open the following " + type + ": Y/N")
        des = input()
        if(des == 'N' or des == 'n'):
            exit()
        elif(des == 'Y' or des == 'y'):
            break
else:
    print("No books or authors with this name")

text_link = 'https://ilibrary.ru' + str(soup.find('li').find('a').get('href')) #Getting link for the text of book or biography
session = requests.get(text_link, headers=HEADERS) #Session for the requests
soup = BeautifulSoup(session.text, 'lxml')
if type == "books":
    print("Make sure author is " + soup.find('div', class_="author").text)
    document = Document()
    document.save('C:\\Users\\nidob\\Projects\\BoAuFinder\\texts\\' + transliterate(soup.find('div', class_='title').find('h1').text) + '.docx')
    file = open('C:\\Users\\nidob\\Projects\\BoAuFinder\\texts\\' + transliterate(soup.find('div', class_='title').find('h1').text) + '.txt', "w", encoding="utf-8")
    file1 = open('C:\\Users\\nidob\\Projects\\BoAuFinder\\texts\\' + transliterate(soup.find('div', class_='title').find('h1').text) + '1.txt', "w", encoding="utf-8")
    print("File for text created")
    print(text_link + '\n' + "page 1")
    # Name of the book and Author---------------------------
    file.write("Автор: " + soup.find('div', id='text').find('div', class_="author").text + '\n')
    file.write("Произведение: " + soup.find('div', class_="title").find('h1').text + '\n')
    file.write("-----------------------------------------" + '\n')
    #------------------------------------------------------
    try:
        amount_of_pages = int(soup.find('span', attrs={'style': 'display:block;text-indent:0em;padding:.6em;font-size:90%;white-space:nowrap'}).text[-1])
    except:
        amount_of_pages = 1
    i = 1
    while i <= amount_of_pages:

        text = soup.find('div', id='text').find_all(['span', 'div'], class_=['p', 'stage'])


        # Characters and stage block-----------------------
        try:          
            characters = soup.find('div', class_="characters").find_all('span', class_="p")
            file.write('\t' + '-' + soup.find('div', class_="characters").find('h5').text + '-' + '\n')
            for person in characters:
                file.write('\t' + person.text)
            file.write('\t' + '-' + soup.find('div', class_='stage').text + '-' + '\n' + '\n')
        except:
            pass
        #--------------------------------------------------


        try:
            file.write('\n' + '\t' +  '---' + soup.find('h2').text + '---' + '\n' + '\n')
        except:
            pass


        # Copying each paragraph---------------------------
        for element in soup.find('div', id = "text").find_all():
            if element.name == "h5":
                file1.write(element.text + '\n')
            if element.get('class') == ['p']:
                try: 
                    writing_with_spaces(element.find('span', class_="person").text, file1)
                    file1.write(element.text[len(element.find('span', class_="person").text):] + '\n')
                except:
                    file1.write(element.text + '\n')
        for paragraph in text:
            try:
                if paragraph.text != soup.find('div', class_="author").text and (paragraph.text not in soup.find('div', attrs={'style': 'text-align: center; text-indent: 0em'}).text) and paragraph['class'] != ['stage']:
                    file.write(paragraph.text + '\n')
                if paragraph['class'] == ['stage'] and (paragraph.text not in soup.find('div', attrs={'style': 'text-align: center; text-indent: 0em'}).text):
                    file.write('-' + paragraph.text + '-' + '\n')
            except:
                file.write(paragraph.text + '\n')
        #--------------------------------------------------


        # Getting next page(if exist)----------------------
        if i + 1 <= amount_of_pages:
            text_link = text_link.replace("p." +  str(i), "p." + str(i + 1))
            print(text_link)
            session = requests.get(text_link, headers=HEADERS) #Session for the requests
            soup = BeautifulSoup(session.text, 'lxml')
            print("page" + str(i + 1))
        i += 1
        #-------------------------------------------------
        
    file.close()
    print("Text copied!")


