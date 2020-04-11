# Test Script
import WebCrawling.collect as WebCrawl

def run_crawl(page):
    if page < 1:
        raise ValueError('Input value should be higher than 1')

    page += 1
    initiate = WebCrawl.Initiate()
    landsite = WebCrawl.WebCrawling()
    driver = initiate.OpenDriver()

    for pg in range(1, page):
        print('\nURL:', str(pg))

        url = 'https://new.land.naver.com/complexes/' + str(pg) + '?ms=37.548119,127.040638,17&a=APT:JGC:ABYG&e=RETAIL'
        landsite.web_open(driver=driver, url=url)
        verify = landsite.web_verify()

        if verify is True:
            landsite.web_collect()
        else:
            print('City is not `서울시`. Please check the URL and try again.')


run_crawl(2)