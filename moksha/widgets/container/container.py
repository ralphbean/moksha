# This file is part of Moksha.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Luke Macken <lmacken@redhat.com>

import uuid
import tw2.core as twc
from tw2.core.resources import encoder
from tw2.jquery import jquery_js
from tw2.jquery.base import jQuery
from tw2.jqplugins.ui.base import jquery_ui_js

from moksha.api.widgets.live import LiveWidget
from moksha.api.widgets.live import subscribe_topics, unsubscribe_topics

container_js = twc.JSLink(filename='static/js/mbContainer.min.js',
                          modname=__name__)
container_css = twc.CSSLink(filename='static/css/mbContainer.css',
                            modname=__name__)
container_resources = twc.DirLink(filename='static/css/elements',
                                  modname=__name__)


# TODO -- this should extend from an as yet unwritten tw2 container (nb?)
# TODO -- should this extend from moksha/api/widgets/containers ?  duplication?
class MokshaContainer(twc.Widget):
    template = 'mako:moksha.widgets.container.templates.container'
    resources = [
        jquery_js, jquery_ui_js, container_js, container_css,
        container_resources,
    ]
    options = ['draggable', 'resizable']
    button_options = ['iconize', 'minimize', 'close']

    draggable = twc.Param(default=True)
    droppable = twc.Param(default=True)
    resizable = twc.Param(default=False)
    iconize = twc.Param(default=True)
    minimize = twc.Param(default=True)
    close = twc.Param(default=True)
    hide = twc.Param(default=True)

    # TODO -- there is a better tw2 idiom for this
    content = twc.Param("TODO == replace this with 'child'", default='')

    widget_name = twc.Param(default=None)
    title = twc.Param(default='Moksha Container')
    skin = twc.Param(default='default') # default, black, white, stiky, alert
    view_source = twc.Param(default=True)
    dock = twc.Param(default='moksha_dock')
    icon = twc.Param(default='gears.png')

    # Pixel tweaking
    width = twc.Param(default=450)
    height = twc.Param(default=500)
    left = twc.Param(default=170)
    top = twc.Param(default=125)

    # Javascript callbacks
    onResize = twc.Param(default=twc.JSSymbol(src="function(o){}"))
    onClose = twc.Param(default=twc.JSSymbol(src="function(o){}"))
    onCollapse = twc.Param(default=twc.JSSymbol(src="function(o){}"))
    onIconize = twc.Param(default=twc.JSSymbol(src="function(o){}"))
    onDrag = twc.Param(default=twc.JSSymbol(src="function(o){}"))
    onRestore = twc.Param(default=twc.JSSymbol(src="function(o){}"))
    _container_options = twc.Variable()

    def prepare(self):
        super(MokshaContainer, self).prepare()
        if isinstance(self.content, twc.widgets.WidgetMeta):
            self.content = self.content.req()

        if isinstance(self.content, twc.Widget):
            self.widget_name = self.content.__class__.__name__
            content_args = getattr(self, 'content_args', {})

            if isinstance(self.content, LiveWidget):
                topics = self.content.get_topics()
                # FIXME: also unregister the moksha callback functions.  Handle
                # cases where multiple widgets are listening to the same topics
                self.onClose = twc.JSSymbol(src="function(o){%s $(o).remove();}" %
                                               unsubscribe_topics(topics))
                self.onIconize = self.onCollapse = twc.JSSymbol(src="function(o){%s}" %
                                                                   unsubscribe_topics(topics))
                self.onRestore = twc.JSSymbol(src="function(o){%s}" %
                                                 subscribe_topics(topics))

            self.content = self.content.display(**content_args)

        for option in self.options:
            # TODO -- inspect this.  It might have become wonky in tw1->tw2
            setattr(self, option, getattr(self, option, True) and option or '')

        self.buttons = ''
        for button in self.button_options:
            if getattr(self, button, True):
                self.buttons += '%s,' % button[:1]

        self.buttons = self.buttons[:-1]

        self.id = str(uuid.uuid4())

        self._container_options = encoder.encode(
            {
                'elementsPath': '/resources/moksha.widgets.container.container/static/css/elements/',
                'onClose': self.onClose,
                'onResize': self.onResize,
                'onCollapse': self.onCollapse,
                'onIconize': self.onIconize,
                'onDrag': self.onDrag,
                'onRestore': self.onRestore,
            }
        )


container = MokshaContainer(id='moksha_container')
