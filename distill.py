# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import ujson
from os import listdir
from os.path import isfile, join
onlyfiles = [ f for f in listdir('data/person/') if isfile(join('data/person',f)) ]
people = {}
for f in onlyfiles:
    with open('data/person/' + f, 'r') as fi:
        try:
            j = ujson.loads(fi.read())
            lowest_degree = 99999
            degree_type = ""
            for d in j['degrees']:
                x = d['graduated_year']
                if x == None:
                    continue
                if x < lowest_degree:
                    lowest_degree = x
                    degree_type = d['degree_type']
            if lowest_degree != 99999:
                people[f] = {'age':(2014 - lowest_degree + 22)}
                if degree_type in ["MD", "Doctoral", "Graduate", "Doctorate", "PHD", "PhD", "phd", "Ph.D.", "Ph.D", "Post Graduate"]:
                    people[f]['age'] += 11
                elif degree_type in ["MBA", "mba"]:
                    people[f]['age'] += 5
                elif degree_type in ["JD", "jd"]:
                    people[f]['age'] += 5
                elif degree_type in ["MS", "MA", "Masters"]:
                    people[f]['age'] += 2
                elif degree_type == "":
                    degree_type = "NA"

                d = degree_type.replace(",","")
                people[f]['degree_type'] = d
                companies = []
                for d in j['relationships']:
                    if "ounder" in d['title']:
                        companies.append(d['firm']['permalink'])
                people[f]['companies'] = companies
        except Exception as e:
            print f
            print e
            continue

for person, value in people.iteritems():
    earliest_fundraise = 9999
    earliest_amount = "NA"

    for c in value['companies']:
        try:
            with open('data/company/' + c.replace(' ','-') + '.js', 'r') as f:
                c = ujson.loads(f.read())

                for r in c['funding_rounds']:
                    try:
                        if r['funded_year'] < earliest_fundraise:
                            earliest_fundraise = r['funded_year']
                            earliest_amount = r['raised_amount']
                    except Exception as e:
                        print e
                        continue
        except Exception as e:
            continue

    if earliest_fundraise == 9999:
        earliest_fundraise = "NA"
    if earliest_amount == None:
        earliest_amount = "NA"
    value['earliest_fundraise'] = earliest_fundraise
    value['earliest_amount'] = earliest_amount

with open('ages.csv', 'a') as f:
    f.write('person,age,degree,amount,date,age_at_fundraise\n')
    for person, value in people.iteritems():
        try:
            f.write("%s,%s,%s,%s,%s,%s\n" % (person, value['age'], value['degree_type'], value['earliest_amount'], value['earliest_fundraise'], (int(value['age']) - (2014 - int(value['earliest_fundraise'])))))
        except Exception as e:
            print e
            print person, value
            continue
        

# <codecell>


# <codecell>


# <codecell>


