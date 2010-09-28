from sqlalchemy.ext.sqlsoup import SqlSoup

import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq

try: 
    sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db?charset=utf8&use_unicode=0', echo=True)
except:
    sql_db.rollback()
    raise

def crawler(storage_list, **keywords):

    site_id = sql_db.site.filter(sql_db.site.site_nm==keywords['site_id']).first()
    br = keywords['mecha_state']

    print "processing list views..."
    for links in storage_list:
        br.follow_link(links)
        d = pq(br.response().read()) 
        post = d(keywords['content']).eq(0).text()
        linky = links.text

        l_title = unicode(linky, 'latin-1').encode('utf-8')

        matches = re.compile(keywords['post_regex']).findall(links.url)
        print "-------------------------------------------------"
        if matches:
            sku = "%s:%s" % (keywords['site_id'], matches[0])
            print "sku: %s" % (sku)
        print "scraping entry: %s, url: %s" % (l_title, links.url)
        #print "scraping contents: %s" % (post)
        try:
            print "extracting post id for sku..."
            if matches:
                print "extraction successful!!"
                sku = "%s:%s" % (keywords['site_id'], matches[0])
                print "checking if we already have a record for this sku..."
                my_list = sql_db.data_prep.filter(sql_db.data_prep.list_sku==sku).first()
            else:
                print "failure in sku extraction..."
                sys.exit()
          
            if my_list:
                print "sku exists!"
                title = my_list.list_title
                text  = my_list.list_text

                print "checking for new title..." 
                if title != l_title:
                    print "title has been updated! updating now..."
                    my_list.list_title = l_title
                else:
                    print "title remains unchanged..."
 
                print "checking for updated post..."
                #print "type for text: %s" % (type(text))
                #print "type for post: %s" % (type(post))
                if text.decode('utf-8') != post:
                    print "post has been updated! updating now..."
                    my_list.list_text = post
                else:
                    print "post remains unchanged..."

                sql_db.commit()
            else:
                print "\bnew sku! inserting into data preparation table."
                sql_db.data_prep.insert(list_sku=sku, list_title=l_title, list_text=post, site_id=site_id.site_id, list_url=links.url)
                sql_db.commit()
                print "insertion successful!"
        except Exception, err:
            print "something went wrong! rolling back table! ERROR: %s" % (str(err))
            sql_db.rollback()

        br.back()

    print "processing done!"

def process_list_view(storage_list, br, pq, content, site_id):
    print "processing list views..."
    for links in storage_list:
        link_html = br.follow_link(links)
        d = pq(link_html.response().read()) 
        post = d(content).eq(0).text()
        linky = links.text
        print "-------------------------------------------------"
        print "scraping entry: %s, url: %s" % (linky, links.url)
        print "scraping contents: %s" % (post)
    
        try:
            print "scraping entry: %s, url: %s" % (linky, links.url)
            my_list = sql_db.listings.filter(sql_db.listings.listings_sku==sku).first()

            if my_list:
                title = my_list.listingstitle
                text  = my_list.listingstext

                if title != links.title:
                    my_list.listingstitle = links.title
                    
                if text != links.post:
                    my_list.listingstext = links.post

                sql_db.commit()
            else:
                sql_db.listings.insert(listingstitle=linky, listingstext=post, site_id=site_id, listingsurl=links.url)
                sql_db.commit()


            my_list = sql_db.listings.filter_by(listingstitle=linky, site_id=site_id).first()
            if not my_list:
                sql_db.listings.insert(listingstitle=linky, listingstext=post, site_id=site_id, listingsurl=links.url)
                sql_db.commit()
        except:
            sql_db.rollback()
   
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
        """
        try:
            print "scraping entry: %s, url: %s" % (linky, url)
            my_list = sql_db.listings.filter_by(listingstitle=linky, site_id=site_id).first()
            if not my_list:
                sql_db.listings.insert(listingstitle=linky, listingstext=post, site_id=site_id, listingsurl=url)
                sql_db.commit()
            else: 
        except:
            sql_db.rollback()
        """
        br.back()
    print "processing done!"

def natural(text):
    matches = re.compile('([0-9]+[Kk]|[0-9]{11})').findall(text)
    return matches
