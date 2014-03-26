import requests
from multiprocessing import Pool
import ujson
import random

url = 'http://api.crunchbase.com/v/1'

def scrape(company):
    with open('data' + company.replace('\n', '') + '.js', 'r') as c:
        c = ujson.loads(c.read())
        relationships = c['relationships']
        for r in relationships:
            if "ounder" in r['title']:
                founder = r['person']['permalink']
                with open('getfounder', 'r') as getem:
                    for line in getem.readlines():
                        if founder in line:
                            continue

                r = requests.get(url + '/person/' + founder + '.js?api_key=35rb9mv76h5xgngw4mtprpfx')
                if r.status_code != 200:
                    #print founder + " BAD"
                    continue
                else:
                    print " GETTING " + founder
                    with open('getfounder', 'a') as getem:
                        getem.write(founder + '\n')
                        getem.close()

                with open('data/person/' + founder + '.js', 'w') as js:
                    js.write(r.content)
                    js.close()


while True:
    print "starting"
    try:
        pool = Pool(50)
        results = []
        with open('companies', 'r') as getem:
            x = getem.readlines()
            for company in x:
                if "groupme" in company:
                	print "WORD"
           # 	scrape(company)
                results.append([pool.apply_async(scrape, ([company]))])

            for result in results:
                timeout = [l.get(9999999) for l in result]
    except Exception as e:
        print e
        break
        continue
