import re
import json
import requests
import logging

from urllib.parse import unquote
from src.conf.headersConf import KuGouHeaders
from src.extractor import *
from src.log import log_config

class Kugou():
    """
    Kugou
    """
    
    def __init__(self):
        self.logger = log_config("Kugou Main")

    def __search(self, keyword:str, page:int, pagesize:int) ->dict[str, tuple[str, str]]:
        keyword = EncodeToUrl(keyword).encode()
        search_url = "http://mobilecdn.kugou.com/api/v3/search/song"
        params = {
            "format": "json",
            "keyword": f"{keyword}",
            "page": f"{page}",
            "pagesize": f"{pagesize}",
            "showtype": "1",
        }
        # 防止ASCII中`%`转义
        params["keyword"] = unquote(params["keyword"])
        
        music_list:dict = dict()
        for pages in range(page+1):
            # update the pages
            params["page"] = f"{pages}"
            resp = requests.get(search_url, headers=KuGouHeaders.SearchHd, params=params)
            # print(resp.text+"\n")
            self.logger.debug(f"send GET to the `{resp.url}`")
            result = json.loads(resp.text)["data"]["info"]
            
            for id in range(pagesize):
                now_data = result[id]
                song_filename = now_data["filename"]
                song_hash = now_data["hash"]
                song_mvhash = now_data["mvhash"]
                music_list.update({f"{song_filename}":(song_hash, song_mvhash)})
        self.logger.debug(len(music_list))
        self.logger.debug("Searching is Done!")
        return music_list

    def search(self, keyword:str, page:int =1, pagesize:int =20) ->dict[str, tuple[str, str]]:
        """
        Search for the music\n
        :param: keyword 搜索词
        :param: page 页数
        :param: pagesize 每页数量

        :return: defaultdict[filename, (hash, mvhash)]
        """
        return self.__search(keyword=keyword, page=page, pagesize=pagesize)        

    def __get_music_by_hash(self, hash:str) ->tuple[str, str]:
        url = "http://m.kugou.com/app/i/getSongInfo.php"
        params = {
            "cmd": "playInfo",
            "hash": hash,
        }
        self.logger.debug("Getting music by hash...")
        resp = requests.get(url=url, params=params, headers=KuGouHeaders.MusicHd)
        song_url = resp.json()["url"]
        song_name = resp.json()["fileName"]
        self.logger.debug("Getting music url is Done!")
        return (song_name, song_url)
    
    def get_music_by_hash(self, hash:str) ->tuple[str, str]:
        """
        Get the music url by hash\n
        
        :param: hash 哈希值
        :return: tuple[song_name, song_url]
        """
        return self.__get_music_by_hash(hash=hash)
    
    def __get_mv_by_hash(self, mv_hash:str, h_quality:bool) ->str:
        url = "http://m.kugou.com/app/i/mv.php"
        params ={
            "cmd": "100",
            "hash": mv_hash,
            "ismp3": "1",
            "ext": "mp4",
        }
        self.logger.debug("Getting the MV now...")
        resp = requests.get(url=url, headers=KuGouHeaders.MusicHd, params=params)
        if h_quality:
            info = resp.json()["mvdata"]["rq"]["downurl"]
            # info = resp.json()["mvdata"]["sq"]["downurl"]
        else:
            info = resp.json()["mvdata"]["le"]["downurl"]        
        self.logger.debug("Getting the MV is Done!")
        return info
    
    def get_mv_by_hash(self, mv_hash:str, h_quality:bool =False) ->str:
        """
        Get the MV Url by MV hash\n
        :param: mv_hash MV哈希值
        :param: h_quality 是否启用更高品质的MV
        :return: mv_url
        """
        return self.__get_mv_by_hash(mv_hash=mv_hash, h_quality=h_quality)
    
