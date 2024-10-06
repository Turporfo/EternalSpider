import random
import os

def ua_load() -> str:
    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/user_agents.txt", 'r') as uas:
        data = uas.readlines()
    return str(data[random.randint(1,900)]).replace('\n','')

class KuGouHeaders():
    # define headers
    SearchHd = {
        # 'Content-Type': 'application/json',
        'Referer': 'https://www.kugou.com/',
        'User-Agent': ua_load(),
    }

    MusicHd = {
        # 'Content-Type': 'application/json',
        'Referer': 'https://www.kugou.com/',
        'User-Agent': ua_load(),
        'Cookie': ''
    }


class KuWoHeaders():

    SEARCH_HEADER = {
        "Host": "www.kuwo.cn",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    MUSIC_BY_ID_HEADER = {
        "Host": "antiserver.kuwo.cn",
        "User-Agent": ua_load(),
    }

    MUSIC_BY_PLAYLIST_HEADER = {
        "Host": "www.kuwo.cn",
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    
    @staticmethod
    def search_header(list)->dict:
        KuWoHeaders.SEARCH_HEADER.update({"Referer": f"https://www.kuwo.cn/search/list?key={list}"})
        return KuWoHeaders.SEARCH_HEADER