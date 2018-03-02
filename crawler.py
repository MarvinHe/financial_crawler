import datetime
from requests_html import HTMLSession

def get_exchanges():
    url = "https://www.exchange-rates.org/MajorRates.aspx"
    session = HTMLSession()
    result = session.get(url)
    trs = result.html.find(".table", first=True).find("tr")
    
    currency_names = [th.find("a")[1].text for th in trs[0].find("th") if th.text != ""]
    country2cnt = {}
    for tr in trs[1:]:
        tds = tr.find("td")
        country = tds[0].find("a", first=True).attrs['title']
        country2cnt[country] = [td.text for td in tds[1:]]
    c2c = {}
    for country, values in country2cnt.items():
        for i, value in enumerate(values):
            c2c[country + ":" + currency_names[i]] = value
    return c2c


if __name__ == "__main__":
    c2c = get_exchanges()
    with open("exchanges.log-{}".format(datetime.datetime.now().strftime("%Y%m%d%H%M")), "w") as out:
        for name, rate in c2c.items():
            out.write("{}\t{}\n".format(name, rate))

