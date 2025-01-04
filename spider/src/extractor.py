import requests
import subprocess
import os
import re
from itertools import chain
from tqdm import tqdm
from src.conf.headersConf import KuGouHeaders
from src.log import log_config
from urllib import parse



logger = log_config("Extractor")

PATH = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_PATH:str =os.path.join(PATH.split("\\spider")[0], 'download')

def quote(string:str, hidden:bool=False):
    """处理字符串"""
    assert string

    string = re.sub(r'[-]', '_', string)
    # 去除非法字符
    if re.search(r'[^\w@%+=:,./]', string, re.ASCII) is not None:
        # string = "'" + string.replace("'", "'\"'\"'") + "'"
        string = re.sub(r"[^\w@%+=:;',./]", '', string)

    
    # 去除多余的空格
    string = re.sub(r'\s+', '', string)
    if hidden and len(string) > 12:
        string = string[:12]+"..."
    return string



def download(url:str, filename:str ='', folder:str ='', format:str ="mp3", cookie:str='') -> None:
    """下载函数"""
    
    path:str = DOWNLOAD_PATH
    logger.info("Start downloading……")
    logger.debug(f"download:{url}")
    
    fileText = requests.get(url, headers=KuGouHeaders.MusicHd, stream=True)
    logger.debug(f'requests.get: {url}')
    if not os.path.exists(path):
        os.mkdir(path)
    total = int(fileText.headers.get('content-length', 0))

    if folder == '':
        folder = f"{path}/{filename}.{format}"
    
    
    logger.debug(f"tqdm: write in {filename}")
    try:
        with tqdm(
            desc=f"\nWriting in {filename}.{format}…",
            total=total,
            ncols=100,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            with open(folder, 'wb') as f:
                for data in fileText.iter_content(chunk_size=1024):
                    f.write(data)
                    bar.update(len(data))
                bar.close()
    except IOError:
        logger.error("ERROR!YOU ARE GETTING A IOERROR!")
    logger.info("Download Successfully!")



class EncodeToUrl:
    '''转码'''
    def __init__(self, string) -> None:
        self.string = string
        
    def encode(self, code:str='utf-8') -> str:
        '''中文转Url'''
        return parse.quote(self.string.encode(code))
    
    def urlEncode(self):
        return parse.urlencode(self.string)
    


def mv2music(mvName:str) -> None:
    '''mv2music'''
    mv_path = os.path.join(DOWNLOAD_PATH, mvName)
    path = os.path.join(PATH.split("\\src")[0], 'tool','ffmpeg.exe')
    mv = '.'.join([mv_path,"mp4"])
    music = '.'.join([mv_path,"mp3"])
    print(path,'-i',mv,'-f','mp3','-vn',music)
    subprocess.call([path,'-i',mv,'-f','mp3','-vn',music])
    
    # ffmpeg -i test.mp4 -f mp3 -vn test.mp3

def xmerge(list1, list2)->tuple:
    return tuple(chain.from_iterable(zip(list1, list2)))

def get_simple_key(dict):
    return list(dict.keys())[0]

def get_simple_value(dict):
    return list(dict.values())[0]

def is_site(site, str):
    if site in str:
        return True
    else:
        return False


