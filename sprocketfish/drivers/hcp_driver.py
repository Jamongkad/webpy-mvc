import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from dataprocess import process_list_view

def main():
    url = 'http://s3.zetaboards.com/HCP/site/'

    br = mechanize.Browser(factory=mechanize.RobustFactory())  
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    print "entering hcp site..."
    print "logging into site..."
    br.open(url)
    br.select_form(nr=0)
    br['uname'] = 'jamongkad'
    br['pw'] = 'password'
    br.submit()

    processing = True
    page = 1
    while(processing):
        req = br.click_link(text='Parts & Accessories')
        res = br.open(req)
        if page is 1:
            print "scraping page 1"
            listings = pq(res.read())
            storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
            process_list_view(storage_list, br, pq, 'td.c_post', 2)
            page = 2
            br.back()
        else:
            print "scraping page 2"
            req_pg_2 = br.find_link(text='2')
            res_pg_2 = br.follow_link(req_pg_2)
            listings = pq(res_pg_2.read())
            storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
            process_list_view(storage_list, br, pq, 'td.c_post', 2)
            processing = False
            br.back()

if __name__ == "__main__":
    main()
