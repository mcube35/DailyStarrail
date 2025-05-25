import httpx
import mweb
import os

USED_REDEEM_FILE = "used_redeem.txt"

def get_used_redeem():
    if not os.path.exists(USED_REDEEM_FILE):
        return set()
    
    try:
        with open(USED_REDEEM_FILE, "r", encoding="utf8") as f:
            return {line.strip() for line in f if line.strip()}
    except Exception as e:
        print(f"[오류] 파일 열기 실패!:\n{e}")
        return set()

def get_new_redeems(session: httpx.Client):
    url = "https://honkai-star-rail.fandom.com/wiki/Redemption_Code"
    res = session.get(url=url)
    if not res: return []

    soup = mweb.get_soup(res)

    tr_list = soup.select("div.mw-content-ltr.mw-parser-output > table > tbody tr")

    new_redeem = []
    used_redeem_list = get_used_redeem()
    for tr in tr_list:
        if not tr.select_one("td.bg-new.text-background"): continue

        redeem_tag = tr.select_one("td:nth-child(1) > b > code")
        if not redeem_tag: continue

        redeem = redeem_tag.getText(strip=True)

        if redeem and not redeem in used_redeem_list:
            new_redeem.append(redeem)
            
    return new_redeem


if __name__ == "__main__":
    session = mweb.session()
    get_new_redeems(session=session)