import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from dataprocess import gt_process_list_view

url = "http://grupotoyota.com.ph/board/"

br = mechanize.Browser(factory=mechanize.RobustFactory())  
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
print "entering GT site..."
print "logging into site..."
br.open(url)
br.select_form(nr=0)
br['username'] = 'jamongkad'
br['password'] = 'p455w0rd'
br.submit()
print "login in successful!"

html = pq(br.response().read())
selling_link = html('a[href*="./viewforum.php?f=8"]').map(lambda i, e: pq(e).attr('href'))[0]
req = br.find_link(url=selling_link)
res = br.follow_link(req)
listings_html = pq(res.read())
sales_urls = listings_html('td.row1 > img[src*="topic"]').parents('td.row1').siblings('td.row1 > a.topictitle').\
             map(lambda i, e: br.find_link(url=pq(e).attr('href')))
gt_process_list_view(sales_urls, br, pq, 'div.postbody', 4)


