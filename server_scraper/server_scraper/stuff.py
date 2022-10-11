good_links = [('https://shoals.craigslist.org', '35630'), ('https://dothan.craigslist.org', '36301'), ('https://kenai.craigslist.org', '99611'), ('https://fairbanks.craigslist.org', '99701'), ('https://juneau.craigslist.org', '99801'), ('https://yuma.craigslist.org', '85364'), ('https://sierravista.craigslist.org', '85635'), ('https://fortsmith.craigslist.org', '72904'), ('https://humboldt.craigslist.org', '95549'), ('https://monterey.craigslist.org', '93940'), ('https://susanville.craigslist.org', '96130'), ('https://santamaria.craigslist.org', '93454'), ('https://imperial.craigslist.org', '92227'), ('https://westslope.craigslist.org', '81501'), ('https://eastco.craigslist.org', '80861'), ('https://nwct.craigslist.org', '06796'), ('https://pensacola.craigslist.org', '32501'), ('https://lakecity.craigslist.org', '32055'), ('https://keys.craigslist.org', '33042'), ('https://orlando.craigslist.org', '32801'), ('https://columbusga.craigslist.org', '31901'), ('https://honolulu.craigslist.org', '96822'), ('https://lewiston.craigslist.org', '83501'), ('https://twinfalls.craigslist.org', '83301'), ('https://quincy.craigslist.org', '62301'), ('https://bloomington.craigslist.org', '47405'), ('https://siouxcity.craigslist.org', '51105'), ('https://iowacity.craigslist.org', '52240'), ('https://swks.craigslist.org', '67901'), ('https://ksu.craigslist.org', '66502'), ('https://westky.craigslist.org', '42038'), ('https://eastky.craigslist.org', '41622'), ('https://shreveport.craigslist.org', '71108'), ('https://houma.craigslist.org', '70360'), ('https://maine.craigslist.org', '04922'), ('https://westmd.craigslist.org', '21502'), ('https://westernmass.craigslist.org', '01011'), ('https://up.craigslist.org', '49855'), ('https://holland.craigslist.org', '49423'), ('https://marshall.craigslist.org', '56258'), ('https://natchez.craigslist.org', '39120'), ('https://stjoseph.craigslist.org', '64501'), ('https://stlouis.craigslist.org', '63110'), ('https://kalispell.craigslist.org', '59901'), ('https://billings.craigslist.org', '59101'), ('https://scottsbluff.craigslist.org', '69361'), ('https://grandisland.craigslist.org', '68801'), ('https://reno.craigslist.org', '89501'),
              ('https://lasvegas.craigslist.org', '89101'), ('https://nh.craigslist.org', '03256'), ('https://southjersey.craigslist.org', '08360'), ('https://farmington.craigslist.org', '87401'), ('https://lascruces.craigslist.org', '88001'), ('https://clovis.craigslist.org', '88101'), ('https://chautauqua.craigslist.org', '14757'), ('https://potsdam.craigslist.org', '13676'), ('https://newyork.craigslist.org', '10007'), ('https://plattsburgh.craigslist.org', '12901'), ('https://longisland.craigslist.org', '11779'), ('https://asheville.craigslist.org', '28801'), ('https://wilmington.craigslist.org', '28401'), ('https://bismarck.craigslist.org', '58501'), ('https://cincinnati.craigslist.org', '45212'), ('https://ashtabula.craigslist.org', '44004'), ('https://lawton.craigslist.org', '73501'), ('https://oregoncoast.craigslist.org', '97459'), ('https://eastoregon.craigslist.org', '97814'), ('https://meadville.craigslist.org', '16335'), ('https://allentown.craigslist.org', '18104'), ('https://greenville.craigslist.org', '29601'), ('https://rapidcity.craigslist.org', '57701'), ('https://nesd.craigslist.org', '57274'), ('https://memphis.craigslist.org', '38103'), ('https://cookeville.craigslist.org', '38501'), ('https://elpaso.craigslist.org', '79901'), ('https://bigbend.craigslist.org', '79834'), ('https://lubbock.craigslist.org', '79401'), ('https://delrio.craigslist.org', '78840'), ('https://wichitafalls.craigslist.org', '76301'), ('https://mcallen.craigslist.org', '78501'), ('https://sanmarcos.craigslist.org', '78666'), ('https://brownsville.craigslist.org', '78520'), ('https://waco.craigslist.org', '76701'), ('https://stgeorge.craigslist.org', '84770'), ('https://ogden.craigslist.org', '84401'), ('https://vermont.craigslist.org', '05401'), ('https://swva.craigslist.org', '24266'), ('https://winchester.craigslist.org', '22601'), ('https://olympic.craigslist.org', 'no zip code'), ('https://spokane.craigslist.org', '99201'), ('https://washingtondc.craigslist.org', '20560'), ('https://huntington.craigslist.org', '25701'), ('https://martinsburg.craigslist.org', '25401'), ('https://eauclaire.craigslist.org', '54701'), ('https://wyoming.craigslist.org', '82501')]

headers = {
    'referer': 'https://duckduckgo.com/,',
    'sec-ch-ua': '\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
}


def get_base_url(url):
    key = '/'
    l = 0
    base_url = ''
    for c in url:
        if c == key:
            l += 1
            if l == 3:
                break
        base_url += c
    return base_url


USER_AGENTS = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
]
