from bs4 import BeautifulSoup
import codecs
import glob
import json


schools = list()
for filename in glob.glob('html/*.html'):
    print 'file: %s' % filename
    soup = BeautifulSoup(open(filename), 'lxml')
    for tag in soup.find('table', class_='education').tbody.find_all('tr'):
        #extract the school data
        if len(tag.find_all('th')) > 0:
            school = {
                    'private':
                    str(tag.find_all('th')[0].get_text()
                        .split(',')[0].__contains__('(P)')),
                    'name':
                    tag.find_all('th')[0].get_text()
                    .split(',')[0].replace('(P)','').strip(),
                    'county': tag.find_all('th')[0].get_text()
                    .strip().split(',')[-1],
                    'number': tag.find_all('th')[1].string.strip(),
                    'percentage': tag.find_all('th')[2].string.strip(),
                    'destination': {}}
            schools.append(school)
            # for the uni/iot row
        elif len(tag.find_all('td')) > 0:
            # take advantage of the fact that this is still a reference
            school['destination'][tag.find_all('td')[0].string.strip()] = tag.find_all('td')[1].string.strip()
        else:
            print '\n no td or tr \n \n'
with codecs.open('schools.json','w',encoding='utf-8') as jsonfile:
    json.dump(schools, jsonfile, ensure_ascii=False, indent=2, sort_keys=True)

with codecs.open('schoolsdupe.json','w',encoding='utf-8') as jsonfile:
    output = list()
    for s in schools:
        for d in s['destination'].keys():
            line = {
                'name': s['name'],
                'private': s['private'],
                'county': s['county'],
                'totalnumber': s['number'],
                'percentage': s['percentage'],
                'destination': d,
                'destinationnumber': s['destination'][d]}
            output.append(line.copy())
    json.dump(output, jsonfile, ensure_ascii=False, indent=2,
            sort_keys=True)
