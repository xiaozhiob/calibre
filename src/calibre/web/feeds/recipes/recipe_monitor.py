#!/usr/bin/env  python

__license__   = 'GPL v3'
__copyright__ = '2009, Darko Miletic <darko.miletic at gmail.com>'

'''
monitorcg.com
'''

import re
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup, Tag

class MonitorCG(BasicNewsRecipe):
    title                 = 'Monitor online'
    __author__            = 'Darko Miletic'
    description           = 'News from Montenegro'
    publisher             = 'MONITOR d.o.o. Podgorica'
    category              = 'news, politics, Montenegro'    
    oldest_article        = 15
    max_articles_per_feed = 150
    no_stylesheets        = True
    encoding              = 'utf-8'
    use_embedded_content  = False
    language              = _('Montenegrin')
    lang                  ='sr-Latn-Me'
    INDEX                 = 'http://www.monitorcg.com'
    
    extra_css = '@font-face {font-family: "serif1";src:url(res:///opt/sony/ebook/FONT/tt0011m_.ttf)} @font-face {font-family: "sans1";src:url(res:///opt/sony/ebook/FONT/tt0003m_.ttf)} body{font-family: serif1, serif} .article_description{font-family: sans1, sans-serif}'
    
    conversion_options = {
                          'comment'          : description
                        , 'tags'             : category
                        , 'publisher'        : publisher
                        , 'language'         : lang
                        , 'pretty_print'     : True
                        }
     
    preprocess_regexps = [(re.compile(u'\u0110'), lambda match: u'\u00D0')]

    keep_only_tags = [dict(name='div', attrs={'id':'ja-current-content'})]

    remove_tags = [ dict(name=['object','link','embed'])
                  , dict(attrs={'class':['buttonheading','article-section']})]

    def preprocess_html(self, soup):
        soup.html['xml:lang'] = self.lang
        soup.html['lang']     = self.lang
        mlang = Tag(soup,'meta',[("http-equiv","Content-Language"),("content",self.lang)])
        mcharset = Tag(soup,'meta',[("http-equiv","Content-Type"),("content","text/html; charset=utf-8")])
        soup.head.insert(0,mlang)
        soup.head.insert(1,mcharset)
        return self.adeify_images(soup)

    def parse_index(self):
        totalfeeds = []
        soup = self.index_to_soup(self.INDEX)
        cover_item = soup.find('div',attrs={'class':'ja-catslwi'})
        if cover_item:
           dt = cover_item['onclick'].partition("location.href=")[2]
           curl = self.INDEX + dt.strip("'")
           lfeeds = [(u'Svi clanci', curl)]
        for feedobj in lfeeds:
            feedtitle, feedurl = feedobj
            self.report_progress(0, _('Fetching feed')+' %s...'%(feedtitle if feedtitle else feedurl))
            articles = []
            soup = self.index_to_soup(feedurl)
            contitem = soup.find('div',attrs={'class':'article-content'})
            if contitem:
                img = contitem.find('img')
                if img:
                   self.cover_url = self.INDEX + img['src']
                for item in contitem.findAll('a'):
                    url         = self.INDEX + item['href']
                    title       = self.tag_to_string(item)
                    articles.append({
                                          'title'      :title
                                         ,'date'       :''
                                         ,'url'        :url
                                         ,'description':''
                                        })
                totalfeeds.append((feedtitle, articles))
        return totalfeeds

        