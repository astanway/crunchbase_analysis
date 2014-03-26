import requests
from multiprocessing import Pool


url = 'http://api.crunchbase.com/v/1'

def scrape(company):
    c = company.split(',')
    if c[0] == 'permalink':
        return

    with open('companies', 'r') as getem:
        for line in getem.readlines():
            if c[0] in line:
                # print "Already have " + c[0]
                return

    r = requests.get(url + c[0] + '.js?api_key=35rb9mv76h5xgngw4mtprpfx')
    if r.status_code != 200:
        print c[0] + " BAD"
        return
    else:
        print "GETTING " + c[0]
        with open('companies', 'a') as getem:
            getem.write(c[0] + '\n')
            getem.close()

        with open('data' + c[0] + '.js', 'w') as js:
            js.write(r.content)
            js.close()


while True:
    try:
        with open('companies.csv', 'r') as f:
            pool = Pool(20)
            print "starting"
            results = []
            for company in f.readlines():
                results.append([pool.apply_async(scrape, ([company]))])

            for result in results:
                timeout = [l.get(9999999) for l in result]
    except:
        continue
