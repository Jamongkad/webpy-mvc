from sqlalchemy.ext.sqlsoup import SqlSoup

import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq

try: 
    sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)
except:
    sql_db.rollback()
    raise

def process_list_view(storage_list, br, pq, content, site_id):
    print "processing list views..."
    for links in storage_list:
        br.follow_link(links)
        d = pq(br.response().read()) 
        post = d(content).eq(0).text()
        linky = links.text
        print "-------------------------------------------------"
        print "scraping entry: %s, url: %s" % (linky, links.url)
        print "scraping contents: %s" % (post)
        print "-------------------------------------------------"
        """
        try:
            print "scraping entry: %s, url: %s" % (linky, links.url)
            my_list = sql_db.listings.filter_by(listingstitle=linky, site_id=site_id).first()
            if not my_list:
                sql_db.listings.insert(listingstitle=linky, listingstext=post, site_id=site_id, listingsurl=links.url)
                sql_db.commit()
        except:
            sql_db.rollback()
        """
        br.back()
    print "processing done!"

def gt_process_list_view(storage_list, br, pq, content, site_id):
    print "processing list views..."
    for links in storage_list:
        br.follow_link(links)
        d = pq(br.response().read()) 
        post = d(content).eq(0).text()
        linky = links.text
        link_url = links.url
        reformed_url = link_url.split('./')[1]
        url = "http://grupotoyota.com.ph/board/%s" % (reformed_url)
        print "-------------------------------------------------"
        print "scraping entry: %s, url: %s" % (linky, url)
        print "scraping contents: %s" % (post)
        print "-------------------------------------------------"
        """
        try:
            print "scraping entry: %s, url: %s" % (linky, url)
            my_list = sql_db.listings.filter_by(listingstitle=linky, site_id=site_id).first()
            if not my_list:
                sql_db.listings.insert(listingstitle=linky, listingstext=post, site_id=site_id, listingsurl=url)
                sql_db.commit()
        except:
            sql_db.rollback()
        """
        br.back()
    print "processing done!"

