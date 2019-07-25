# -*- coding: UTF-8 -*-
from collective.diazotheme.bootstrap.browser.homepage import HomepageView as baseview
from five import grok
from my315ok.products.product import Iproduct
from plone.memoize.instance import memoize
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone.resources import add_bundle_on_request
from Products.CMFPlone.resources import add_resource_on_request
from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone.utils import safe_unicode
from xtcs.policy import _
from xtcs.policy.browser.interfaces import IThemeSpecific
from zope.component import getMultiAdapter

import cgi


# add_resource_on_request(self.request, 'jquery.recurrenceinput')
# add_bundle_on_request(self.request, 'thememapper')


# grok.templatedir('templates')

class FrontpageView(baseview):

    #     grok.context(ISiteRoot)
    #     grok.template('homepage')
    #     grok.name('index.html')
    #     grok.layer(IThemeSpecific)
    #     grok.require('zope2.View')

    def __init__(self, context, request):
        # Each view instance receives context and request as construction
        # parameters
        self.context = context
        self.request = request
#         add_bundle_on_request(self.request, 'homepage-legacy')

    def escape(self, value):
        """Extended escape"""
        value = cgi.escape(value, True)
        return value.replace("'", "&apos;")

    @memoize
    def seo(self):
        "seo keywords output"
        keywords = u"湖南齐德,齐德,齐德集团,齐德企业管理"
        keywords = safe_unicode(keywords)
        output = u"""<meta name="keywords" content="%s"/>""" % (
            self.escape(keywords))
        return output

    @memoize
    def comments(self):
        "seo comments output"
        comments = u"湖南齐德企业管理有限公司简称:湖南齐德,齐德集团.公司位于湘潭(国家级)经济开发区，下辖湘潭名生置业有限公司、湘潭市德佑置业有限公司两家房地产开发公司、湘潭水电工程有限公司、湘潭永固建材有限公司四家公司，现正在与恒大集团合作开发“湘潭•书香门第”小区项目。公司资产大，负债少，队伍小，绩效优，是一家成长性非常好、很有希望上市的公司。"
        comments = safe_unicode(comments)
        output = u"""<!--%s-->""" % (self.escape(comments))
        return output

    def carouselid(self):
        return "carouselid"

    def active(self, i):
        if i == 0:
            return "active"
        else:
            return ""

    @memoize
    def carouselresult(self):

        out = """
        <div id="carousel-generic" class="carousel slide">
  <!-- Indicators -->
  <ol class="carousel-indicators">
    <li data-target="#carousel-generic" data-slide-to="0" class="active"></li>
    <li data-target="#carousel-generic" data-slide-to="1"></li>
    <li data-target="#carousel-generic" data-slide-to="2"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div class="item active">
      <img src="http://www.xtcs.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtcs.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtcs.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-generic" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="#carousel-generic" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>

</div>
        """

        braindata = self.catalog()({'object_provides': Iproduct.__identifier__,
                                    'b_start': 0,
                                    'b_size': 3,
                                    'path': '/qidejt/qidedongtai/tupianxinwen',
                                    'sort_order': 'reverse',
                                    'sort_on': 'created'})

        brainnum = len(braindata)
        if brainnum == 0:
            return out

        outhtml = """<div id="%s" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
        """ % (self.carouselid())
        outhtml2 = '</ol><div class="carousel-inner">'
        for i in range(brainnum):
            out = """<li data-target='%(carouselid)s' data-slide-to='%(indexnum)s' class='%(active)s'>
            </li>""" % dict(indexnum=str(i),
                            carouselid=''.join(['#', self.carouselid()]),
                            active=self.active(i))

            outhtml = ''.join([outhtml, out])   # quick concat string
            objurl = braindata[i].getURL()
            linkurl = braindata[i].linkurl
            if not bool(linkurl):
                linkurl = objurl
            objtitle = braindata[i].Title
            outimg = """<div class="%(classes)s">
                        <a href="%(linkurl)s"><img class="img-responsive" style="%(css)s" src="%(imgsrc)s" alt="%(imgtitle)s"/></a>
                          <div class="carousel-caption">
                            <h3>%(imgtitle)s</h3>
                              </div>
                                </div>""" % dict(classes=''.join(["item ", self.active(i)]),
                                                 linkurl=linkurl,
                                                 css="width:100%",
                                                 imgsrc=''.join(
                                                     [objurl, "/@@images/image/preview"]),
                                                 imgtitle=objtitle)
            outhtml2 = ''.join([outhtml2, outimg])   # quick concat string
#        outhtml = outhtml +'</ol><div class="carousel-inner">'
        result = ''.join([outhtml, outhtml2])   # quick concat string
        out = """
        </div><a class="left carousel-control" href="%(carouselid)s" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="%(carouselid)s" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>
</div>""" % dict(carouselid=''.join(["#", self.carouselid()]))
        return ''.join([result, out])


# roll zone


    def rollheader(self):
        return u"新闻"

    def rollmore(self):
        context = self.getOrgnizationFolder()
        return context.absolute_url()


# outer html zone


    def outhtmlheader(self):
        return u"论坛热帖"

    def outhtmlmore(self):
        return "http://plone.315ok.org/"

    def dataparameter(self):
        data = {
            'code': "utf-8",
            'filter': True,
            'target': "http://plone.315ok.org/",
            'tag': "div",
            'cssid': "portal_block_52_content",
            'cssclass': "dxb_bc",
            'attribute': "",
            'regexp': "",
            'index': 0,  # fetch first block
            'interval': 24
        }
        return data

# roll table output
    def getDonateFolder(self):
        from xtcs.policy.interfaces import IJuanzenggongshi
        brains = self.catalog()(
            {'object_provides': IJuanzenggongshi.__identifier__})
        context = brains[0].getObject()
        return context

    def getable(self, view):
        """view: a organization folder object's view name
        call view come from my315ok.socialorgnization orgnization_listing module,
        view name may be "orgnizations_administrative","orgnizations_survey"
        """


#         add_bundle_on_request(self.request, 'homepage-legacy')
        fview = getMultiAdapter((self.context, self.request), name=view)
        # call getMemberList function output table
        # fetch 20 items roll
        return fview.getMemberList(start=0, size=20,)
