from sqlalchemy.ext.sqlsoup import SqlSoup

import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq

try: 
    sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)
except:
    sql_db.rollback()
    raise


def process_list_view(storage_list):
    print "processing list views..."
    for links in storage_list:
        br.follow_link(links)
        d = pq(br.response().read()) 
        post = d('div.postcolor').eq(0).text()
        linky = links.text
        print "scraping entry: %s, url: %s" % (linky, links.url)
        try:
            my_list = sql_db.listings.filter_by(listingstitle=linky, site_id=1).first()
            if not my_list:
                sql_db.listings.insert(listingstitle=linky, listingstext=post, site_id=1, listingsurl=links.url)
                sql_db.commit()
        except:
            sql_db.rollback()
        br.back()
    print "processing done!"

def main():

    url = 'http://www.jdmunderground.ph/'
    br = mechanize.Browser(factory=mechanize.RobustFactory())  
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    print "entering jdmu site..."
    print "logging into site..."
    br.open(url)

    br.select_form(nr=0) 
    br['UserName'] = 'jamongkad'
    br['PassWord'] = 'p455w0rd'
    br.submit()

    processing = True
    page = 1
    while(processing):
        print "going to Underground Parts"
        req = br.click_link(text='Underground Parts')
        res = br.open(req)
        if page is 1: 
            print "scraping page 1"
            listings = pq(res.read())
            lists = listings('td.darkrow1').eq(5).parents('tr').siblings('tr').children('td > a[href*="showtopic"]').not_('.linkthru')
            storage_list = lists.map(lambda i, e: br.find_link(text=pq(e).text().replace("  ", " ")))
            process_list_view(storage_list)
            page = 2
            br.back()
        else:
            print "scraping page 2"
            req_pg_2 = br.find_link(text='2')
            res_pg_2 = br.follow_link(req_pg_2)
            listings_2 = pq(res_pg_2.read())
            storage_list_2 = listings_2('td.row4 > a[href*="showtopic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
            process_list_view(storage_list_2)
            processing = False

if __name__ == "__main__":
    main()
