from bs4 import BeautifulSoup
import requests

url = 'https://hymnary.org/hymn/GG2013/725'
result = requests.get(url).text
doc = BeautifulSoup(result, 'html.parser')


# first_line = doc.find(class_='hy_infoItem').string

trs = doc.find_all(class_='result-row')
# print((trs[0].parent).contents[3])

# (trs[0].parent).contents[3] == First Line: && O Jesus, I have promised && and link (https://hymnary.org/text/o_jesus_i_have_promised)

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
        else:
            info[key_name] = td[2].a.string
    
print(info)


info = {
    'First Line:': 'O Jesus, I have promised', 
    'Title:': 'O Jesus, I Have Promised', 
    'Author:': 'John Ernest Bode', 
    'Meter:': '7.6.7.6.D', 
    'Language:': 'English', 
    'Publication Date:': '2013', 
    'Scripture:': '1 Samuel 3:10', 
    'Topic:': '(4 more...)', 
    'Name:': 'NYLAND', 
    'Adapter and Harmonizer:': 'David Evans', 
    'Key:': 'E♭ Major', 
    'Source:': 'Finnish folk melody', 
    'Copyright:': 'Adapt. and Harm.© 1927 Oxford University Press', 
    'Notes:': '(alternate tune: ANGEL’S STORY, 724)', 
    'Audio recording:': None}