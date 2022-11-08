import requests
from pyquery import PyQuery as pq
import os
import sys
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='recursively download whole FTP directories',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-u','--url', metavar='URL', type=str, help='the url you want to download') 
    parser.add_argument('-o','--outdir', metavar='OUTDIR', default="./",type=str, help='The directory where the downloaded files are placed') 
    return parser

def download_file(url, path):
    if os.path.exists(path):
        print('File exists !!! : ', path)
    else:
        response = requests.get(url)
        with open(path, 'wb') as f:
            f.write(response.content)
            f.close()
        print('Download completed !!! : ', path)

def get_dir(old_url,new_url):
    old_url=old_url.strip('/')
    new_url=new_url.strip('/')
    #print(old_url,new_url)
    dir=new_url[len(old_url)+1:-1]
    return dir

def get_url(page_url,outdir):
    try:
        doc = pq(url=page_url,encoding='utf-8')
    except:
        print("Error! "+ " Something Wrong! Please check if the url is valid: " + page_url)
        sys.exit(100)
    a_links = doc.find('a') #get the file or directory
    for a in a_links.items():
        href = a.attr('href')
        name = a.text()
        if href == '../' or href == './' in href:
            continue
        else:
            if href[-1] == '/':   # when directory
                new_url = os.path.join(page_url, name)
                dir = get_dir(page_url,new_url)  #get the relative path
                if os.path.exists(dir)==False:
                    os.makedirs(dir)
                get_url(new_url)
            else:   # when file
                path = os.path.join(page_url, name)
                name = path[29:]
                download_file(path, name)
                # print(os.path.join(page_url, href))

def main(): 
    parser = get_parser()
    args = vars(parser.parse_args())

    if not args['url']:
        parser.print_help()
        return

if __name__ == '__main__':
    main()
