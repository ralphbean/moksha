import logging
import os
import errno
import sys
import pprint

from pkg_resources import EntryPoint, iter_entry_points, resource_string

import tw2.core as twc
import tw2.core.core

log = logging.getLogger(__name__)

def import_widget(path):
    """Import a widget given a dotted or entry point notation path.

    Can import both widget instances or classes.

       >>> import_widget('tw2.core.Widget')
       <class 'tw2.core.Widget'>
       >>> import_widget('tw2.core:Widget')
       <class 'tw2.core.Widget'>
       >>> import_widget('os.popen')

    """
    if ':' not in path:
        parts = path.split('.')
        path = '.'.join(parts[:-1]) + ':' + parts[-1]
    widget = EntryPoint.parse("x="+path).load(False)
    if not isinstance(widget, (twc.WidgetMeta, twc.Widget)):
        widget = None
    return widget


def widget_path(widget):
    """Returns the path of a widget instance or subclass

    >>> from tw2.core import Widget
    >>> widget_path(Widget)
    'tw2.core.Widget'
    >>> widget_path(Widget())
    'tw2.core.Widget'
    """
    if not isinstance(widget, (twc.WidgetMeta, twc.Widget)):
        raise TypeError("Only widgets are allowed")
    if isinstance(widget, twc.Widget):
        widget = widget.__class__
    return '.'.join([widget.__module__, widget.__name__])

def format_code(code, format='python'):
    """Formats a chunk of code as html. If pygments is installed it will
    pygmentize it.
    
    >>> code = "from __future__ import teletransportation"
    >>> '<pre' in format_code(code)
    True
    """
    try:
        from pygments import highlight, formatters, lexers
    except ImportError:
        log.info("Pygments is not available to colorize")
        return '<pre>' + code + '</pre>'
    lexer = lexers.get_lexer_by_name(format)
    formatter = formatters.get_formatter_by_name('html')
    return highlight(code, lexer, formatter)

#TODO: Memoize this function
def widget_template(widget, extension='.html'):
    """Returns the template of a widget as a string.

    Loads external templates if needed.

    >>> from widgetbrowser.tests.widgets import *
    >>> widget_template(TestWidgetExternalTemplate())
    'Dummy template $value\\n'

    If more than one is available, it will use the extension to disambiguate.

    >>> from widgetbrowser.tests.widgets import TestWidgetExternalTemplate
    >>> widget_template(TestWidgetMultipleExternalTemplate(), '.html')
    'Dummy template $value\\n'
    >>> widget_template(TestWidgetMultipleExternalTemplate(), '.mak')
    'Dummy template $value mako version\\n'
    """
    template = widget.template
    if template:
        # Template seems to refer to a file, look it up
        parts = template.split('.')
        possible_extensions = set(".html .mak .mako".split())
        possible_extensions.remove(extension)
        possible_extensions = [extension] + list(possible_extensions)
        for ext in possible_extensions:
            try:
                return resource_string('.'.join(parts[:-1]), parts[-1]+ext)
            except IOError, e:
                if e.errno not in (0, errno.ENOENT):
                    raise
        return None
    return template

def pretty_print(obj):
    """Pretty prints an object returning pygmentized code if possible."""
    return format_code(pprint.pformat(obj), 'python')

def display_widget(widget, argstr='', ctx=None):
    """Displays a widget with optional arguments as a string.
    

    .. warning:: IT IS VERY UNSAFE TO EXECUTE UNTRUSTED CODE

    Example::

        >>> from tw2.core import Widget, Param
        >>> class TestWidget(Widget):
        ...     params = ['param']
        ...     template = "$value-$param"
        >>> display_widget(TestWidget())
        u'None-None'
        >>> display_widget(TestWidget(), '"hello", param=2')
        u'hello-2'
    """
    ctx = ctx or {}
    ctx['_w'] = widget
    code = "_o = _w(%s)" % argstr
    exec code in ctx
    return ctx['_o']

def widget_url(widget, action='', prefix=None):
    """Returns the URL of the controller to perform `action` on `widget`.

    If no `prefix` is passed the it will be tried to be fetched from
    `tw2.core.request_local` where the :class:`WidgetBrowser` leaves it
    on every request.

    Example::

        >>> import tw2.core as twc
        >>> widget_url(twc.Widget)
        '/tw2.core.Widget/'
        >>> widget_url(twc.Widget())
        '/tw2.core.Widget/'

    You can also pass the `path` of the widget::

        >>> widget_url('tw2.core.Widget')
        '/tw2.core.Widget/'
        >>> widget_url('tw2.core.Widget', 'show')
        '/tw2.core.Widget/show'
        >>> widget_url('tw2.core.Widget', 'show', prefix='/widget')
        '/widget/tw2.core.Widget/show'

    .. note::

        You can pass any path the widget can be imported from when passing a
        string but if you pass a widget instance or subclass then the real
        module where it is defined will be generated.
    """
    if isinstance(widget, (twc.Widget, twc.WidgetMeta)):
        widgeturi = widget_path(widget)
    else:
        widgeturi = widget
        if import_widget(widgeturi) is None:
            return
    if prefix is None:
        prefix = getattr(tw2.core.core.request_local, 'browser_prefix', '')
    return '/'.join([prefix.rstrip('/'), widgeturi, action])

def all_widgets():
    """Iterates over all the Widget subclasses in the modules
    that are declared as `toscawidgets.widgets` entrypoints

    >>> len(list(all_widgets())) > 0
    True
    """
    seen = set()
    for ep in iter_entry_points('tw2.widgets'):
        try:
            mod = ep.load(False)
        except ImportError, e:
            log.error("Could not load %r: %s", ep, e)
            continue
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, twc.WidgetMeta) and obj not in seen:
                seen.add(obj)
                yield obj

class WidgetParameters(object):
    """Wraps a widget and provides information on it's parameters.

    Example::

        >>> from tw2.core import Widget
        >>> params = WidgetParameters(Widget)
        >>> len(params.all) > 0
        True
        >>> params.all - params.local == params.inherited
        True
    """
    def __init__(self, widget):
        if isinstance(widget, Widget):
            widget = widget.__class__
        self.widget = widget
        self.all = widget.params
        self.inherited = set()
        for b in self.widget.__mro__:
            if b is self.widget:
                continue
            self.inherited.update(getattr(b, 'params', set()))
        self.local = self.all - self.inherited

    def get_default(self, name, default=None):
        """Returns a string representation of a parameter default value.

        Example::

            >>> from tw2.core import Widget
            >>> params = WidgetParameters(Widget)
            >>> type(params.get_default('id'))
            <type 'str'>
        """
        return repr(getattr(self.widget, name, default))

    def get_doc(self, name, default='Undocumented'):
        """Returns parameters's doc. If it is not documented it will return
        ``default``

        Example::

            >>> from tw2.core import Widget
            >>> params = WidgetParameters(Widget)
            >>> type(params.get_doc('id'))
            <type 'str'>
        """
        return getattr(self.widget, name + '__doc', default)
        
def build_docs(src, dst):
    import sphinx
    if not os.path.exists(dst):
        os.mkdir(dst)
    return sphinx.main(['sphinx-build', src, dst])
