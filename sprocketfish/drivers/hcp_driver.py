from sqlalchemy.ext.sqlsoup import SqlSoup
from dataprocess import crawler
import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq

#try: 
#    sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db?charset=utf8&use_unicode=0', echo=True)
#except:
#    sql_db.rollback()
#    raise
#
#def process_list_view(storage_list):
#    print "processing list views..."
#    for links in storage_list:
#        br.follow_link(links)
#        d = pq(br.response().read()) 
#        post = d('td.c_post').eq(0).text()
#        linky = links.text
#
#        l_title = unicode(linky, 'latin-1').encode('utf-8')
#
#        matches = re.compile('HCP\/topic\/(\d+)/').findall(links.url)
#        print "-------------------------------------------------"
#        if matches:
#            sku = "HCP:%s" % (matches[0])
#            print "sku: %s" % (sku)
#        print "scraping entry: %s, url: %s" % (l_title, links.url)
#        #print "scraping contents: %s" % (post)
#        """ NOTES:
#        Look for edited title posts in td.cat-title > div.description
#        For content edits td.c_post > div.editby
#        """
#        try:
#            print "checking sku..."
#            if matches:
#                print "sku is existing!"
#                sku = "HCP:%s" % (matches[0])
#                print "checking if sku exists..."
#                my_list = sql_db.data_prep.filter(sql_db.data_prep.list_sku==sku).first()
#            else:
#                print "no sku found exiting..."
#                sys.exit()
#          
#            if my_list:
#                print "sku exists!"
#                title = my_list.list_title
#                text  = my_list.list_text
#                
#                try:
#                    print "checking for new title..." 
#                    if title != l_title:
#                        print "title has been updated! updating now..."
#                        my_list.list_title = l_title 
#                    else:
#                        print "title remains unchanged..."
#     
#                    print "checking for updated post..."
#                    if text != post:
#                        print "post has been updated! updating now..."
#                        my_list.list_text = post
#                    else:
#                        print "post remains unchanged..."
#
#                    sql_db.commit()
#                except:
#                    print "something went wrong with data update!"
#                    sql_db.rollback()
#            else:
#                print "new sku! inserting into data preparation table."
#                sql_db.data_prep.insert(list_sku=sku, list_title=l_title, list_text=post, site_id=2, list_url=links.url)
#                sql_db.commit()
#                print "insertion successful!"
#        except Exception, err:
#            print "something went wrong! rolling back table! ERROR: %s" % (str(err))
#            sql_db.rollback()
#
#        br.back()
#    print "processing done!"
#
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
regex = 'HCP\/topic\/(\d+)/'
c_content = 'td.c_post'
while(processing):
    print "going to Parts & Accessories"
    req = br.click_link(text='Parts & Accessories')
    res = br.open(req)
    if page is 1:
        print "scraping page 1"
        listings = pq(res.read())
        storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
        crawler(storage_list, mecha_state=br, content=c_content, post_regex=regex, site_id='HCP')
        #process_list_view(storage_list)
        page = 2
        br.back()
    else:
        print "scraping page 2"
        req_pg_2 = br.find_link(text='2')
        res_pg_2 = br.follow_link(req_pg_2)
        listings = pq(res_pg_2.read())
        storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
        crawler(storage_list, mecha_state=br, content=c_content, post_regex=regex, site_id='HCP')
        #process_list_view(storage_list)
        processing = False
        br.back()
