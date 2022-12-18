'''
allows you to receive files from the lms.mai website
YOU NEED TO MANUALLY GET THE "MoodleSession" COOKIE FROM THE LMS
'''
import os
import time
import random
import re
import requests
from ftfy import fix_encoding
def get_mai_files(url, dirname=".", cookies=None):
    '''
    download files from moodle to dirname/<filename>
    '''
    mainresponse = requests.get(url,
                            timeout=10, cookies=cookies)
    for cur_str in mainresponse.text.split('\n'):
        if re.search(r"Файл", cur_str):
            ser = re.findall("href=\"(.*?)\"",cur_str)
            # print(ser)
            for url_i in ser:
                # delay in order not to run into LMS limits
                time.sleep(random.random()+1)
                getfile(url_i,cookies=cookies,dirname=dirname)
                    # exit()
def getfile(url, cookies=None, dirname="."):
    '''
    get file from url
    '''
    response = requests.get(url,cookies=cookies,timeout=10)
    filename = response.headers.get('Content-Disposition')
    if filename:
        regmatch = re.search(r".*?\"(.*)\"",filename)
        filename = fix_encoding(regmatch.group(1))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(dirname+'/'+filename,"wb") as f:
            f.write(response.content)
            print(filename)
if __name__ == "__main__":
    cookies1 = {'MoodleSession': '<SESSIONID>'}
    get_mai_files("https://lms.mai.ru/course/view.php?id=<ID>",
                  dirname="<DIRNAME>",
                  cookies=cookies1)
