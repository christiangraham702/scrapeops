from server_scraper.stuff import state_links


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


def get_num_listings(x):
    return None if x[:1] == '\n' else x


def get_price(x):
    if x:
        return x.replace('$', '').replace(',', '')
    else:
        return 0


def is_listings(response):
    if response.xpath('//span[@class="totalcount"]/text()').get():
        return True
    else:
        return False


def get_state(link, query_length):
    link = link[:-abs(query_length)]
    w = ''
    for state in state_links:
        for l in state_links[state]:
            if link == l:
                w = state
    return w
