import httpx
from bs4 import BeautifulSoup as bs

def get_soup(res):
    return bs(res.text, 'html.parser')

def session() -> httpx.Client:
    try:
        return httpx.Client(
            http2=True,
            headers = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                # "sec-ch-ua": 'Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99',
            }
        )
    except Exception as e:
        print(f'[오류] 세션을 가져오던도중 오류가 발생하였습니다:\n{e}')
        return None