import tw2.core as twc
from tw2.jquery import jquery_js

jquery_jgrowl_js = twc.JSLink(
    filename='static/jquery.jgrowl.js',
    modname=__name__)
jquery_jgrowl_css = twc.CSSLink(
    filename='static/jquery.jgrowl.css',
    modname=__name__)

class MokshaNotificationWidget(twc.Widget):
    resources = [jquery_js, jquery_jgrowl_js, jquery_jgrowl_css]

moksha_notify = MokshaNotificationWidget(id='moksha_notify')
