from bs4 import BeautifulSoup
import requests

url = 'https://hymnary.org/hymn/GG2013/726'
result = requests.get(url).text
doc = BeautifulSoup(result, 'html.parser')

trs = doc.find_all(class_='result-row')

info = {}
scriptures = []
for tr in trs:
    for td in [tr.contents]:
        key_name = td[0].span.string
        if td[2].span.string:
            info[key_name] = td[2].span.string
        elif key_name == 'Scripture:':
            for i in range(len(td[2].span.contents)):
                scripture_values = td[2].span.contents[i].string
                if '; ' in scripture_values:
                    pass
                else:
                    scriptures.append(scripture_values)
                    info[key_name] = scriptures
        elif key_name == 'Topic:':
            info[key_name] = f'{td[2].span.contents[0].string} {td[2].span.span.string}'.split('; ')
        elif key_name == 'Audio recording:':
            info[key_name] = td[2].a.get('href')
        else:
            info[key_name] = td[2].a.string
    
print(info)

text = doc.find('div', id = "text")

print(text)

# Create a Hymn Model
# Use the information to create a new Hymn to your database
#   If data is tune, change that key to 'tune name' like Sarah did in the pokemon app
# db.add and db.commit


info = {
    'First Line:': 'Will you come and follow me if I but call your name?', 
    'Title:': 'Will You Come and Follow Me (The Summons)', 
    'Author:': 'John L. Bell', 
    'Meter:': '13.13.7.7.13', 
    'Language:': 'English', 
    'Publication Date:': '2013', 
    'Scripture:': ['Isaiah 6:8', 'Matthew 4:19', 'Matthew 8:22', 'Matthew 16:24-26', 'Matthew 19:27-30', 'Mark 1:16-21', 'Mark 8:34-38', 'Luke 5:1-11', 'Luke 9:23-26', 'Luke 9:61-62', 'Luke 19:1-10', 'John 1:41-42', 'John 10:27-30', 'John 12:24-26', 'John 20:21', 'John 21:15-19'], 
    'Topic:': ['Commitment', 'Discipleship and Mission', 'Invitation ', 'Ministry', 'Service'], 
    'Copyright:': 'Arr. © 1987 WGRG, Iona Community (admin. GIA Publications, Inc.)', 
    'Name:': 'KELVINGROVE', 
    'Arranger:': 'John L. Bell', 
    'Key:': 'F Major', 
    'Source:': 'Scottish melody', 
    'Audio recording:': 'https://hymnary.org/media/fetch/150503/hymnary/audio/GG2013/726-WillYourCome_accomp.mp3'}