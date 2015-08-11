from lxml import html
import requests
import time
from collections import OrderedDict
import csv
from matplotlib.pylab import plt
import numpy as np

def serialize_data(dictionary, filename):
    orderedEntries = OrderedDict(sorted(dictionary.items(), key=lambda x: x[1]))
    with open(filename, 'wb') as f:
        w = csv.writer(f, dialect = 'excel')
        w.writerow(['Number', 'Time (h)'])
        for k,v in orderedEntries.iteritems():
            w.writerow([k,v])

def get_position(num, entries):
    orderedEntries = OrderedDict(sorted(entries.items(), key=lambda x: x[1]))
    nEntries = len(orderedEntries.keys())
    idx = orderedEntries.keys().index(num)
    print "Position: " + str(idx+1) + " out of " + str(nEntries)

def get_entries(pages, gender):
    entries = {}
    for j in xrange(1, pages+1):
        try:
            page = requests.get('http://results.prudentialridelondon.co.uk/2015/?page=' + str(j) + '&event=I&num_results=100&pid=list&search%5Bsex%5D=' + gender)
            tree = html.fromstring(page.text);

            for i in xrange(1,100):
                number = int(tree.xpath('//*[@id="cbox-left"]/div[6]/div[1]/table/tbody/tr[' + str(i) + ']/td[1]/text()')[0])
                time_string = tree.xpath('//*[@id="cbox-left"]/div[6]/div[1]/table/tbody/tr[' + str(i) + ']/td[12]/text()')[0]
                t = time.strptime(time_string,"%H:%M:%S")
                tot = float(t.tm_sec)/3600.0 + float(t.tm_min)/60.0 + t.tm_hour
                entries.update({number:tot})

            print "{0} of {1}".format(j, pages)
        except Exception as e:
            print e.message

    return entries

def plot_histogram(entries):
    n, bins, patches = plt.hist(entries.values(), 50, normed=1, facecolor='green', alpha=0.75)

    plt.xlabel('Time (h)')
    plt.ylabel('Probability')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    m_entries = get_entries(206, 'M')
    f_entries = get_entries(51, 'W')

    # Serialize data
    serialize_data(m_entries,'RideLondon100_2015_M_ranked_results.csv')
    serialize_data(f_entries,'RideLondon100_2015_W_ranked_results.csv')
    serialize_data(dict(m_entries.items() + f_entries.items()),'RideLondon100_2015_ranked_results.csv')

    # Generate histograms
    plot_histogram(m_entries)
    plot_histogram(f_entries)




