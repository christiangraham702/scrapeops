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
        return x.replace('$', '')
    else:
        return None


def is_listings(response):
    if response.xpath('//span[@class="totalcount"]/text()').get():
        return True
    else:
        return False
