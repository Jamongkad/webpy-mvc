from sqlalchemy.ext.sqlsoup import SqlSoup
from dataprocess import crawler, test_crawler
import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq

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
end_pge_cnt = 3

regex = 'HCP\/topic\/(\d+)/'
c_content = 'td.c_post'
site = 'HCP'
while(processing):
    print "going to Parts & Accessories"
    req = br.click_link(text='Parts & Accessories')
    res = br.open(req)
    if page is 1:
        print "scraping page 1"
        listings = pq(res.read())
        storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
        crawler(storage_list, mecha_state=br, content=c_content, post_regex=regex, site_id=site, reform_url=False)
        page += 1
        br.back()
    else:
        print "scraping page %s" % (page)
        req_pg_2 = br.find_link(text='%s' % (page))
        res_pg_2 = br.follow_link(req_pg_2)
        listings = pq(res_pg_2.read())
        storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
        crawler(storage_list, mecha_state=br, content=c_content, post_regex=regex, site_id=site, reform_url=False)
        page += 1
        br.back()
        
        if(page == end_pge_cnt):
            processing = False
