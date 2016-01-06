import argparse
import re
from multiprocessing import Pool
import requests
import bs4

index_url = 'http://vchart.yinyuetai.com/vchart/month'

def get_video_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    return [a.attrs.get('href') for a in soup.select('div.search-rank_L a[href^=http://v.yinyuetai.com/video]')]

#print(get_video_page_urls())


def get_video_data(video_page_url):
    video_data = {}
    response = requests.get(video_page_url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    video_data['title'] = unicode(soup.title.string)
    video_data['title'] = video_data['title'].strip()
    video_data['url'] = unicode(video_page_url)
    return video_data

def parse_args():
    parser = argparse.ArgumentParser(description='Show Yinyuetai top 10 video statistics.')
    parser.add_argument('--max', metavar='MAX', type=int, help='show the top MAX entries only.')
    parser.add_argument('--csv', action='store_true', default=False, help='output the data in CSV format.')
    parser.add_argument('--workers', type=int, default=4,
                        help='number of workers to use, 4 by default.')
    return parser.parse_args()

def show_video_stats(options):
    pool = Pool(options.workers)
    video_page_urls = get_video_page_urls()
    results = pool.map(get_video_data, video_page_urls) 
    max = options.max
    if max is None or max > len(results):
        max = len(results)
    if options.csv:
        print(u'"title","url"')
    else:
        print(u'Title (url)')
    for i in range(max):
        if options.csv:
            print(u'"{0}","{1}"' .format( results[i]['title'],results[i]['url']))
        else:
            print(u'{0:60} ({1:36})' .format( results[i]['title'], results[i]['url']))

if __name__ == '__main__':
    show_video_stats(parse_args())
