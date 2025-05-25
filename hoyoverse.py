from redeem_crawler import *
import json
import time
import mweb
import os

class Hoyoverse:
    def __init__(self):
        self.session = mweb.session()

    def use_redeem(self, redeem: str, uid: str, cookie_token: dict):
        res = self.session.post(
            url = "https://public-operation-hkrpg.hoyoverse.com/common/apicdkey/api/webExchangeCdkeyRisk",
            cookies = cookie_token,
            data = json.dumps({
                "lang":"ko",
                "game_biz":"hkrpg_global",
                "uid": uid,
                "region":"prod_official_asia",
                "cdkey": redeem,
                "platform":"4",
            }),
        )
        return res


    def daily_check(self, cookie_token: dict):
        url_list = ["https://sg-public-api.hoyolab.com/event/luna/hkrpg/os/sign", "https://sg-public-api.hoyolab.com/event/luna/hkrpg/os/resign"]
        for url in url_list:
            res = self.session.post(
                url = url,
                cookies = cookie_token,
                data = json.dumps({
                    "lang":"ko",
                    "act_id":"e202303301540311"
                }),
            )
            print(res.text)
            time.sleep(5)


    def use_redeem_by_wiki(self, uid:str, cookie_token: dict):
        redeem_list = get_new_redeems(hoyoverse.session)
        if not redeem_list:
            print("[정보] 사용할 수 있는 새 리딤 코드가 없습니다.")
            return
        
        for redeem in redeem_list:
            try:
                res = hoyoverse.use_redeem(
                    redeem=redeem,
                    uid=uid,
                    cookie_token=cookie_token
                )
                res.raise_for_status()
                data = res.json()
            except Exception as e:
                print(f"[오류] 코드 '{redeem}' 처리 중 예외 발생: {e}")
                continue

            print(f"{redeem} => {data}")
            time.sleep(5)
    


if __name__ == "__main__":
    hoyoverse = Hoyoverse()
    cookie_token = json.loads(os.getenv("COOKIE_TOKEN"))

    hoyoverse.use_redeem_by_wiki(uid=os.getenv("UID"), cookie_token=cookie_token)
    hoyoverse.daily_check(cookie_token)