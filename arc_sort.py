import sys
import argparse
import urllib.request

from tqdm import tqdm
from bs4 import BeautifulSoup

BASE_URL = 'http://www.mai-net.net'
#Arcadia掲示板の総ページ数, かなり余裕があるので当分このままで良さげ
NUMBER_OF_PAGES = 489


def arc_sort(condition, number):
    result = []
    for i in tqdm(range(NUMBER_OF_PAGES)):
        url = BASE_URL + '/bbs/sst/sst.php?act=list&cate=all&page=' + str(i)
        html = urllib.request.urlopen(url).read().decode()
        soup = BeautifulSoup(html, 'html.parser')

        attributes = []
        td = [i.string for i in soup.find_all('td')[14:-3]]
        links = [i.get('href') for i in soup.find_all('a')][23:]
        tmp_atrs = [td[i:i+7] for i in range(0, len(td), 7)]

        for atr, link in zip(tmp_atrs, links):
            atr.append(BASE_URL + link)
            attributes.append(atr)

        [result.append(i) for i in attributes if not None in i]

    if condition < 4:
        if condition == 1:
            sort_condition = '#story'
        elif condition == 2:
            sort_condition = '#impression'
        elif condition == 3:
            sort_condition = '#pv'
        sorted_result = sorted(result, key=lambda x: int(x[condition+2]), reverse=True)
    elif condition == 4:
        sort_condition = '#pv/#story'
        sorted_result = sorted(result, key=lambda x: int(x[5])/int(x[3]), reverse=True)
    elif condition == 5:
        sort_condition = '#impression/#story'
        sorted_result = sorted(result, key=lambda x: int(x[4])/int(x[3]), reverse=True)

    with open('sorted_arc.txt', 'w') as f:
        f.write('Rank Title (Original)\t#Story\t#Impression\tPV\t(sorted by {})\n\n'.format(sort_condition))
        for c, i in enumerate(sorted_result, 1):
            if c < number + 1:
                f.write('{}. {} ({})\t'.format(str(c), i[1], i[0]))
                f.write('{}\t{}\t{}\n{}\n\n'.format(i[3], i[4], i[5], i[7]))


def main():
    parser = argparse.ArgumentParser(description='sort system for Arcadia')
    parser.add_argument('--condition', type=int, default=3,
                        help='condition for sorting \
                        (1:#story, 2:#impression, 3:#pv, 4:pv/story, 5:impression/story \
                        (default=3, sort by the number of pv))')
    parser.add_argument('--number', type=int, default=300,
                        help='the number of output (top n ranks)')
    args = parser.parse_args()

    arc_sort(args.condition, args.number)


if __name__ == '__main__':
    main()
