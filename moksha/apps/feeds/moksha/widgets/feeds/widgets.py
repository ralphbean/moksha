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

"""
:mod:`moksha.widgets.feedtree` - A dynamic feed tree
====================================================

There are currently two implementations of this application, an `ajax` version
and a `live` version.  The ajax version makes a new request to our WSGI server
each time, where as the `live` implementation communicates over a persistent
Stomp-driven Orbited TCPSocket.   The live widget will automatically connect up
to a unique message topic that it uses to communicate with the Moksha Feed
Consumer in the Moksha Hub.  It also listens for changes in the feeds that
it is viewing.

.. widgetbrowser:: moksha.widgets.feedtree.moksha_feedreader
   :tabs: demo, source, template
   :size: x-large

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

from tg import config
import tw2.core as twc
from tw2.jquery import jquery_js
from tw2.jquery.base import jQuery
from tw2.jqplugins.dynatree import DynaTreeWidget
from uuid import uuid4

from moksha.api.widgets.live import LiveWidget

class MokshaAjaxFeedTree(DynaTreeWidget):
    options = {
        'title': 'Moksha Ajax Feed Tree',
        'rootVisible': True,
        'persist': True,
        'initAjax': {
                'url': '/apps/feeds/init_tree',
                'data': {'key': 'root'}
        },
        'onActivate': twc.JSSymbol(src="""
            function(dtnode) {
              $('#TopPane').load(
                  '/apps/feeds/get_entries?key=' + dtnode.data.key.replace(/ /, ''));
            }
        """.replace('\n', ''))
    }


class MokshaAjaxFeedEntriesTree(DynaTreeWidget):
    options = {
        'rootVisible': False,
        'persist': True,
        'onActivate': twc.JSSymbol(src="""
            function(dtnode) {
                $('#BottomPane').load(
                    '/apps/feeds/get_entry?key=' + dtnode.data.key);
            }"""),
    }


class MokshaLiveFeedTree(DynaTreeWidget):
    options = dict(
        title = 'Moksha Live Feed Tree',
        rootVisible = True,
        persist = True,
        fx = {'height': 'toggle', 'duration': 200},
        initAjax = {
                'url': '/apps/feeds/init_tree',
                'data': {'key': 'root'}
        },
        onActivate = twc.JSSymbol(src="""
            function(dtnode) {
                moksha.send_message(
                    'moksha.feeds', {
                        action: 'get_feed',
                        'key': dtnode.data.key,
                        topic: moksha_feed_topic}); }"""))

    def prepare(self):
        self.topic = str(uuid4())
        super(MokshaLiveFeedTree, self).prepare()

class MokshaLiveFeedEntriesTree(DynaTreeWidget):
    options = dict(
        rootVisible = False,
        persist = True,
        onActivate = twc.JSSymbol(src="""
            function(dtnode) {
                moksha.send_message('moksha.feeds', {
                    'action': 'get_entry',
                    'key': dtnode.data.key,
                     topic: moksha_feed_topic
                 });
                /* Unsubscribe from current feed, subscribe to new one */
            }
        """.replace('\n', ''))
    )


## Load our feed tree widgets.
feedtree_engine = config.get('moksha.feedtree.engine', 'live')
if feedtree_engine == 'live':   # Live widgets
    feed_tree = MokshaLiveFeedTree(id='feed_tree')
    feed_entries_tree = MokshaLiveFeedEntriesTree(id='feed_entries_tree')
elif feedtree_engine == 'ajax': # Ajax widgets
    feed_tree = MokshaAjaxFeedTree(id='feed_tree')
    feed_entries_tree = MokshaAjaxFeedEntriesTree(id='feed_entries_tree')

splitter_js = twc.JSLink(filename='static/splitter.js',
                     modname=__name__)

splitter_css = twc.CSSLink(filename='static/main.css',
                       media='all',
                       modname=__name__)


class MokshaFeedReaderWidget(LiveWidget):
    name = 'Moksha Feed Reader'
    params = ['topic']
    topic = 'moksha.feeds' # will get replaced by a unique uuid at render-time
    template = 'mako:moksha.widgets.feeds.templates.feedreader'
    resources = [jquery_js, splitter_js, splitter_css]
    css_class = 'moksha-feedreader'

    # Child widgets.
    feed_tree = twc.Param(default=feed_tree)
    feed_entries_tree = twc.Param(default=feed_entries_tree)

    container_options = {
            'top': 50,
            'left': 50,
            'height': 600,
            'width': 890,
            'icon': 'browser.png',
            }
    onmessage = """
      if (json.action == 'get_feed') {
          var tree = $("#moksha_feedreader_feed_entries_tree").dynatree("getRoot");
          tree.removeChildren();
          tree.append(json.entries);
      } else if (json.action == 'get_entry') {
          $('#BottomPane').html(json.content);
      } else if (json.action == 'new_entry') {
          /* TODO */
          moksha.debug('new_entry!');
      }
    """

    def prepare(self):
        self.topic = str(uuid4()) 
        super(MokshaFeedReaderWidget, self).prepare()
        self.add_call(jQuery('#' + self.id).splitter({
            'splitVertical': True,
            'outline': True,
            'sizeLeft': True,
            'anchorToWindow': True,
            'accessKey': "I",
            }))
        self.add_call(jQuery('#RightPane').splitter({
            'splitHorizontal': True,
            'sizeTop': True,
            'accessKey': "H",
            }))


moksha_feedreader = MokshaFeedReaderWidget(id='moksha_feedreader')
