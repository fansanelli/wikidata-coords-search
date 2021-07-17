#!/usr/bin/env python

###########################################################################
##                                                                       ##
## Copyrights Francesco Ansanelli 2021                                   ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

import csv
import json
import requests
import sys

def query(long, lat):
    url = 'https://query.wikidata.org/sparql'
    query = '''
SELECT ?place ?placeLabel ?location ?dist WHERE {
  SERVICE wikibase:around { 
      ?place wdt:P625 ?location . 
      bd:serviceParam wikibase:center "Point(__LONG__ __LAT__)"^^geo:wktLiteral .
      bd:serviceParam wikibase:radius "0.3" . 
      bd:serviceParam wikibase:distance ?dist.
  } 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "it" }
} ORDER BY ASC(?dist)
'''
    r = requests.get(url, params = {'format': 'json', 'query': query.replace('__LONG__', long).replace('__LAT__', lat)})
    return r.json()

def main():
    if len(sys.argv) < 2:
        print('invalid input file')
        sys.exit(0)
    with open('out.csv', 'w', newline='') as csvout:
        writer = csv.writer(csvout, delimiter=';')
        with open(sys.argv[1], newline='') as csvin:
            reader = csv.reader(csvin, delimiter=';')
            for row in reader:
                if row[4]:
                    coords = row[4].split(',')
                    json = query(coords[1], coords[0])
                    if len(json['results']['bindings']) == 0:
                        print(row[1] + ' (' + row[0] + ') - nessun risultato\n')
                    else:
                        for result in json['results']['bindings']:
                            if input(row[1] + ' (' + row[0] + ') corrisponde a: ' + result['placeLabel']['value'] + ' (' + result['place']['value'] + ') con dist: ' + result['dist']['value'] + '?\n') == "y":
                                writer.writerow([row[0], result['place']['value']])
                                break

if __name__ == "__main__":
    main()

