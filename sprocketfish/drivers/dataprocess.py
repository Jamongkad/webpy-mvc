from sqlalchemy.ext.sqlsoup import SqlSoup

import mechanize, urllib
import cookielib, re, sys
from pyquery import PyQuery as pq
import MultiDict

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
        posts = d(keywords['content']).map(lambda i, e: (pq(e).text(), pq(e).html()))
        authors = d(keywords['author']).map(lambda i ,e: pq(e).text())
        
        post_data = process_post_data(posts, authors, keywords['site_id'])

        linky = links.text

        l_title = unicode(linky, 'latin-1').encode('utf-8')

        (matches, ) = re.compile(keywords['post_regex']).findall(links.url)
        if keywords['reform_url']: 
            link_url = links.url
            reformed_url = link_url.split('./')[1]
            url = "http://grupotoyota.com.ph/board/%s" % (reformed_url)
        else:
            url = links.url

        #debug output
        print "-------------------------------------------------"
        if matches:
            sku = "%s:%s" % (keywords['site_id'], matches)
            print "sku: %s" % (sku)
        print "scraping entry: %s, url: %s" % (l_title, url)

        #database stuff
        try:
            print "extracting post id for sku..."
            if matches:
                print "extraction successful!!"
                sku = "%s:%s" % (keywords['site_id'], matches)
                print "checking record for existing sku..."
                my_list = sql_db.data_prep.filter(sql_db.data_prep.list_sku==sku).first()
            else:
                print "failure in sku extraction..."
                sys.exit()
          
            if my_list:
                print "sku record db exists!"
                title = my_list.list_title

                print "checking for new title..." 
                if title != l_title:
                    print "title has been updated! updating now..."
                    my_list.list_title = l_title
 
                print "checking for updated post..."
                for author in post_data.keys():
                    for idx, p in enumerate(post_data.getall(author)): 
                        post_id = "%s:%s:%s" % (sku, "postid-%s" % idx, author) 
                        existing_post = sql_db.listings_posts.filter(sql_db.listings_posts.idlistings_posts==post_id).first()

                        pst_text = p[0].encode('utf-8')
                        pst_html = p[1].encode('utf-8')

                        if existing_post:
                            if pst_text != existing_post.list_text_text and pst_html != existing_post.list_text_html:
                                existing_post.list_text_text = pst_text
                                existing_post.list_text_html = pst_html
                        else: 
                            print "inserting posts %s" % (post_id)
                            sql_db.listings_posts.insert(idlistings_posts=post_id, list_sku=sku, 
                                                         list_text_text=pst_text, list_text_html=pst_html, list_author=author)
                sql_db.commit()
            else:
                print "new sku! inserting into data preparation table."
                #insert post
                sql_db.data_prep.insert(list_sku=sku, list_title=l_title, site_id=site_id.site_id, list_url=url)
                #insert sub posts and authors
                for author in post_data.keys():
                    for idx, p in enumerate(post_data.getall(author)): 
                        post_id = "%s:%s:%s" % (sku, "postid-%s" % idx, author) 
                        print "inserting posts %s" % (post_id) 
                        sql_db.listings_posts.insert(idlistings_posts=post_id, list_sku=sku, 
                                                     list_text_text=p[0], list_text_html=p[1], list_author=author)
                        #print post_id, p[0]

                sql_db.commit()
                print "insertion successful!"
        except Exception, err:
            print "something went wrong! rolling back table! ERROR: %s" % (str(err))
            sql_db.rollback()
            sys.exit()

        br.back()

    print "processing done!"

def test_crawler(storage_list, **keywords):

    site_id = sql_db.site.filter(sql_db.site.site_nm==keywords['site_id']).first()
    br = keywords['mecha_state']

    print "processing list views..."
    for links in storage_list:
        br.follow_link(links)
        d = pq(br.response().read()) 

        posts = d(keywords['content']).map(lambda i, e: (pq(e).text(), pq(e).html()))
        authors = d(keywords['author']).map(lambda i, e: pq(e).text())
        post_data = process_post_data(posts, authors, keywords['site_id'])
        linky = links.text

        print links.url

        l_title = unicode(linky, 'latin-1').encode('utf-8')

        (matches, ) = re.compile(keywords['post_regex']).findall(links.url)
        if keywords['reform_url']: 
            link_url = links.url
            reformed_url = link_url.split('./')[1]
            url = "http://grupotoyota.com.ph/board/%s" % (reformed_url)
        else:
            url = links.url

        print "---------------------------------------------------"
        if matches:
            site_id = keywords['site_id']
            sku = "%s:%s" % (site_id, matches) 
            print "sku: %s" % (sku)
        print "scraping entry: %s, url: %s" % (l_title, url)

        for i in post_data.keys():
            for idx, p in enumerate(data.getall(i)):
                print idx, i, p
        
        #"""
        #Hmmmm let us see if the site is JDMU or any other car forum that has multiple forum subposts... 
        #"""
        #extra_links = None
        #if keywords['site_id'] is 'JDMU':
        #    (extra_links ,) = d('a[title="Jump to page..."]').eq(1).parents('td').eq(1).map(lambda i, e: re.compile('\([0-9]\)').findall(td.pq(e).text()))
        #    for i in range(1, int(extra_links[1]) + 1):
        #        print i
        #    
        #    extra_links_cnt = int(extra_links[1])

        #   while(extra_links_cnt):
        #                
        #               
        #              
        #       pass
        #       extra_links_cnt -= 1
        #       br.back()
        #br.back()

def find_quote(text):
    match = re.compile('QuoteBegin').findall(text)
    return match

def process_post_data(posts, authors, site_id):
    #remove begin quote cuz stupid pyquery see's it as an seperate entity
    storage = MultiDict.OrderedMultiDict()
    if site_id == 'JDMU': 
        clean_posts = [(post[0], post[1]) for post in posts if not find_quote(post[0])]
    else:
        clean_posts = [(post[0], post[1]) for post in posts]

    for i in range(0, len(authors)):
        storage[authors[i]] = clean_posts[i]

    return storage
