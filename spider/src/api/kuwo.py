import requests
import re
import logging
from urllib.parse import unquote
from typing import Dict
from src.log import log_config
from src.extractor import *
from src.conf.headersConf import KuWoHeaders


class Kuwo():
    """kuwo"""

    def __init__(self):
        self.logger = log_config("Kuwo Main", logging.DEBUG)

    def __search(self, keyword:str, pn:int, rn:int)->dict[str, str]:

        keyword = EncodeToUrl(keyword).encode()
        searchUrl = "https://www.kuwo.cn/search/searchMusicBykeyWord"
        # 例如: https://www.kuwo.cn/search/searchMusicBykeyWord?ft=music&encoding=utf8&mobi=1&pn=0&rn=30&all=%E7%AB%A5%E8%AF%9D%E9%95%87
        params = {
            # 防止搜索词是英文时不返回数据
            "vipver": "1",
            "ft": "music",
            "encoding": "utf8",
            "mobi" : "1",
            "pn": f"{pn}",
            "rn": f"{rn}",
            "all": f"{keyword}",
        }
        # 防止Requests库对`%`进行转义
        params["all"] = unquote(params["all"])
        # 更改headers中的Referer
        SEARCH_HEADER = KuWoHeaders().search_header(list=keyword) 

        music_dict:dict = dict()
        # 防止pn为0时循环不执行:pn+1
        for pns in range(pn+1):
            # 更新前面的页数
            params["pn"] = f"{pns}"
            resp = requests.get(url=searchUrl, headers=SEARCH_HEADER, params=params)
            data = resp.json()
            abslist = data["abslist"]
            # 排除可能存在的数据不等现象
            if len(abslist) != rn:
                rn = len(abslist)
            for item in range(rn):
                lists = abslist[item]
                music_dict.update({f"{lists['SONGNAME']}-{lists['ARTIST']}": lists["MUSICRID"]})
        self.logger.debug(len(music_dict))
        return music_dict  
    
    def search(self, keyword:str, pn:int =0, rn:int =20)->dict[str, str]:
        """
        Kuwo Search Api\n
        :param: keyword 关键字
        :param: pn 页数
        :param: rn 每页个数
        :return: defaultdict类型字典
        """
        return self.__search(keyword=keyword, pn=pn, rn=rn)
    
    def __get_music_by_id(self, rid)->str:

        url = f"http://antiserver.kuwo.cn/anti.s?format=mp3&rid=MUSIC_{rid}&type=convert_url&response=url"
        music_url = requests.get(url,headers=KuWoHeaders.MUSIC_BY_ID_HEADER)
        return music_url.text
    
    def get_music_by_id(self, rid)->str:
        """
        Get the download link for the music by the rid\n
        :param: rid 歌曲rid
        :return: music_url 歌曲下载地址
        """
        return self.__get_music_by_id(rid=rid)
    
    def __get_music_by_playlist(self, playlist:str)->Dict[str, str]:

        resp = requests.get(playlist, headers=KuWoHeaders.MUSIC_BY_PLAYLIST_HEADER)
        # print(resp.text)
        infos = re.compile(r'<div class="song_name flex_c" data-v-3a193997>.*?<a title="(?P<name>.*?)" href="/play_detail/(?P<rid>\d+)"').finditer(resp.text)
        
        music_info={}
        for info in infos:
            song_name = info.group("name")
            song_rid = info.group("rid")
            song_url = self.__get_music_by_id(rid=song_rid)
            music_info.update({song_name:song_url})
        
        return music_info
    
    def get_music_by_playlist(self, playlist_url)->Dict[str, str]:
        """
        Get the download link for the music by the playlist\n

        :param: playlist 歌单下载地址
        :return: 
        """
        return self.__get_music_by_playlist(playlist=playlist_url)
    
    def __get_ranklist(self, ):
        pass

    def get_ranklist(self, ):
        pass

    def __getLyric(self):
        pass