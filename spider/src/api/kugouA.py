"""
Kugou API
"""


import json
import requests
import src.extractor as extractor
from src.conf.headersConf import KuGouHeaders
from src.log import log_config



class Kugou(object):
    """kugou"""

    logger = log_config("Kugou MainA")

    def __init__(self, req:str) -> None:
        """初始化"""
        self.musicHeaders = KuGouHeaders.MusicHd
        self.searchHeaders = KuGouHeaders.SearchHd
        # self.mv2music = mv2music
        self.req = req # 搜索词
        self.encode = extractor.EncodeToUrl


    def _search(self, page:int =1, pagesize:int =20, mvUrl:bool = False) -> tuple:
        """Search for the music
        :params page:搜索页数(该参数得到结果可能不准确)
        :params pagesize:每页歌曲数量
        :params mvUrl:是否获取MV下载地址
        :return 歌曲信息, 歌曲hash, (MV信息) 
        """

        keyword = self.encode(self.req).encode()
        url = f'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={keyword}&page={page}&pagesize={pagesize}&showtype=1'
        Kugou.logger.info(f"Try to search {self.req}……")
        
        res = requests.get(url, headers=self.searchHeaders)

        res = json.loads(res.text)['data']['info']
        Kugou.logger.info("Get information successfully!\n")
        for id, info in enumerate(res):
            print(f'|{id+1}:{info.get("filename")}')
        choice = int(input("请输入要下载音乐的序号："))
        if choice <= 0 and choice > len(res):
            Kugou.logger.error("非法输入!")
            raise ValueError("Error8!非法输入!")
        songInfo = res[choice-1]['filename']
        songHash = res[choice-1]['320hash']
        if mvUrl == True:
            Kugou.logger.info("正在获取MV的hash值……")
            songMV = res[choice-1]["mvhash"]
            Kugou.logger.info("获取成功！")
            return songInfo, songHash, songMV
        Kugou.logger.info("获取成功！")
        return songInfo, songHash

    # def _getMusicWithUrl(self, musicUrl):
    #     if not isinstance(musicUrl, str):
    #         print(f"{musicUrl} isn't a string")

    def _getMusicUrl(self, hash:str):
        """获取音乐地址
        :params hash:歌曲hash值
        """

        musicInfoUrl = f'http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={hash}'
        Kugou.logger.info("正在获取音频……")

        infoRes = requests.get(musicInfoUrl, headers=self.musicHeaders)
        downloadUrl = infoRes.json()["url"]
        if downloadUrl == '':
            Kugou.logger.error("付费歌曲, 尝试通过MV下载音频……")
            return 0
        musicInfo = infoRes.json()["fileName"]
        return downloadUrl, musicInfo



    def _getMvUrl(self, mvHash:str):
        """获取MV下载地址
        :params mvHash: Mv的hash值
        """

        mv = f'http://m.kugou.com/app/i/mv.php?cmd=100&hash={mvHash}&ismp3=1&ext=mp4'
        Kugou.logger.info("正在获取MV……")
        infoMv = requests.get(mv, headers=self.musicHeaders)
        resp = infoMv.json()["mvdata"]["le"]["downurl"]
        return resp

            
    def _getLrc(self, hash):
        """获取歌词"""
        pass