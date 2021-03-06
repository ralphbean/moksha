import moksha.utils

from tg import expose, tmpl_context

class Root(object):

    @expose()
    def index(self, *args, **kwargs):
        return 'Hello World!'

    @expose('mako:demo.templates.template')
    def mako(self, *args, **kwargs):
        """ An example controller method exposed with a Mako template """
        return {'msg': 'Hello World!'}

    @expose('mako:moksha.templates.widget')
    def livewidget(self, *args, **kwargs):
        tmpl_context.widget = moksha.utils.get_widget('live')
        tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
        return dict(options={})

    @expose('mako:demo.templates.model')
    def model(self, *args, **kwargs):
        from demo.model import DBSession, HelloWorldModel
        entries = DBSession.query(HelloWorldModel).limit(10).all()
        return dict(entries=entries)

    @expose('mako:demo.templates.model')
    def cached_model(self, *args, **kwargs):
        from pylons import cache
        mycache = cache.get_cache('helloworld')
        entries = mycache.get_value(key='entries', createfunc=self._get_entries,
                                    expiretime=3600)
        return dict(entries=entries)

    def _get_entries(self, *args, **kwargs):
        from demo.model import DBSession, HelloWorldModel
        return DBSession.query(HelloWorldModel).limit(10).all()
