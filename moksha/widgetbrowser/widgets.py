from moksha.widgetbrowser import util
import string
import tw2.core as twc
from tw2.jquery import jquery_js
from tw2.jqplugins.ui.base import jquery_ui_js

__all__ = ['WidgetBrowserTabs']

mod = __name__
#mod = 'widgetbrowser'
flora_all_css = twc.CSSLink(modname=mod, filename="static/themes/flora/flora.all.css")
tabs_css = twc.CSSLink(modname=mod, filename="static/ui.tabs.css")
wb_css = twc.CSSLink(modname=mod, filename="static/widgetbrowser.css")
pygments_css = twc.CSSLink(modname=mod, filename="static/pygments.css")
widgetbrowser_js = twc.JSLink(modname=mod, filename="static/widgetbrowser.js",
                          location="bodybottom")

httprepl_js = twc.JSLink(modname=mod, filename='static/httprepl.js',
                     location="bodybottom")
httprepl_css = twc.CSSLink(modname=mod, filename="static/httprepl.css")

class WidgetBrowserTabs(twc.Widget):
    template = "genshi:moksha.widgetbrowser.templates.widget_browser_tabs"
    in_sphinx = False
    resources = [jquery_js, jquery_ui_js, widgetbrowser_js,
                 tabs_css, wb_css, pygments_css]
    size = "small"
    tabs = ['demo', 'demo_source', 'source', 'template', 'parameters']
    prefix = None
    
    def prepare(self):
        super(WidgetBrowserTabs, self).prepare()
        self.tabs = [
            (
                string.capwords(t.replace('_', ' ')),
                util.widget_url(self.value, t, prefix=self.prefix)
            ) for t in self.tabs]

        if not self.in_sphinx:
            # Not displayed inside Sphinx, include jquery and pygments
            jquery_js.inject()
            pygments_css.inject()


class WidgetRepl(twc.Widget):
    template = 'mako:moksha.widgetbrowser.teplates.widget_repl'
    prefix = '/_repl/' # show nicely in the browser tabs
    include_dynamic_js_calls = True
    resources = [jquery_js, jquery_ui_js, httprepl_js,
                 httprepl_css, flora_all_css]

    def prepare(self):
        super(WidgetRepl, self).prepare()
        assert self.id, "This widget needs an id"
        config = dict(prefix=self.prefix)
        call = twc.js_function('HTTPRepl.render')('#'+self.id, config)
        self.add_call("jQuery(function () {%s});" %  call)

repl = WidgetRepl(id="widgetrepl")
