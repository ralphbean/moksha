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

import moksha
import moksha.utils

from tg import config
import tw2.core as twc
from tw2.jquery import jquery_js
from paste.deploy.converters import asbool

from moksha.api.widgets.orbited import orbited_host, orbited_port, orbited_url
from moksha.lib.helpers import defaultdict
from moksha.widgets.notify import moksha_notify
from moksha.widgets.json import jquery_json_js

stomp_js = twc.JSLink(link=orbited_url + '/static/protocols/stomp/stomp.js')

def stomp_subscribe(topic):
    """ Return a javascript callback that subscribes to a given topic,
        or a list of topics.
    """
    sub = "stomp.subscribe('%s');"
    if isinstance(topic, list):
        sub = ''.join([sub % t for t in topic])
    else:
        sub = sub % topic
    return sub


def stomp_unsubscribe(topic):
    """ Return a javascript callback that unsubscribes to a given topic,
        or a list of topics.
    """
    sub = "stomp.unsubscribe('%s');"
    if isinstance(topic, list):
        sub = ''.join([sub % t for t in topic])
    else:
        sub = sub % topic
    return sub


class StompWidget(twc.Widget):
    callbacks = ['onopen', 'onerror', 'onerrorframe', 'onclose',
                 'onconnectedframe', 'onmessageframe']
    resources = [jquery_js, jquery_json_js]
    onopen = twc.Param("onopen callback",
                       default=twc.js_callback('function(){}'))
    onerror = twc.Param("onerror callback",
                        default=twc.js_callback('function(error){}'))
    onclose = twc.Param("onclose callback",
                        default=twc.js_callback('function(c){}'))
    onerrorframe = twc.Param("onerrorframe callback",
                             twc.js_callback('function(f){}'))
    onmessageframe = twc.Param("onmessageframe callback",
                               default='')
    onconnectedframe = twc.Param("onconnectedframe callback",
                                default='')

    engine_name = 'mako'
    template = u"""
      <script type="text/javascript">
        if (typeof TCPSocket == 'undefined') {
            moksha_callbacks = new Object();
            moksha_socket_busy = false;
        }

        ## Register our topic callbacks
        % for topic in topics:
            var topic = "${topic}";
            if (!moksha_callbacks[topic]) {
                moksha_callbacks[topic] = [];
            }
            moksha_callbacks[topic].push(function(json, frame) {
                ${onmessageframe[topic]}
            });
        % endfor

        if (typeof TCPSocket == 'undefined') {
            document.domain = document.domain;
            moksha_socket_busy = true;
            $.getScript("${orbited_url}/static/Orbited.js", function(){
                Orbited.settings.port = ${orbited_port};
                Orbited.settings.hostname = '${orbited_host}';
                Orbited.settings.streaming = true;
                TCPSocket = Orbited.TCPSocket;
                $.getScript("${orbited_url}/static/protocols/stomp/stomp.js", function(){
                    ## Create a new TCPSocket & Stomp client
                    stomp = new STOMPClient();
                    stomp.onopen = ${onopen};
                    stomp.onclose = ${onclose};
                    stomp.onerror = ${onerror};
                    stomp.onerrorframe = ${onerrorframe};
                    stomp.onconnectedframe = function(){ 
                        moksha_socket_busy = false;
                        $('body').triggerHandler('moksha.socket_ready');
                        ${onconnectedframe}
                    };
                    stomp.onmessageframe = function(f){
                        var dest = f.headers.destination;
                        var json = null;
                        try {
                            var json = $.parseJSON(f.body);
                        } catch(err) {
                            moksha.error("Unable to decode JSON message body");
                            moksha.error(msg);
                        }
                        if (moksha_callbacks[dest]) {
                            for (var i=0; i < moksha_callbacks[dest].length; i++) {
                                moksha_callbacks[dest][i](json, f);
                            }
                        }
                    };

                    stomp.connect('${stomp_host}', ${stomp_port},
                                  '${stomp_user}', '${stomp_pass}');
                });
            });

        } else {
            ## Utilize the existing stomp connection
            if (moksha_socket_busy) {
                $('body').bind('moksha.socket_ready', function() {
                    ${onconnectedframe}
                });
            } else {
                ${onconnectedframe}
            }
        }

        window.onbeforeunload = function() {
            if (typeof stomp != 'undefined') {
                stomp.reset();
            }
        }

        if (typeof moksha == 'undefined') {
            moksha = {
                /* Send a STOMP message to a given topic */
                send_message: function(topic, body) {
                    stomp.send($.toJSON(body), topic)
                }
            }
        }

        % if notify:
            $.jGrowl.defaults.position = 'bottom-right';
        % endif
      </script>
    """

    # TODO -- what does this do?
    hidden = twc.Param("Undocumented.  What does this do?",
                       default=True)

    notify = twc.Param(
        "Popup notification bubbles on socket state changes",
        default=asbool(config.get('moksha.socket.notify', False)))
    orbited_host = twc.Param(
        "orbited host",
        default=config.get('orbited_host', 'localhost'))
    orbited_port = twc.Param(
        "orbited port",
        default=config.get('orbited_port', 9000))
    orbited_scheme = twc.Param(
        "orbited scheme",
        default=config.get('orbited_scheme', 'http'))
    orbited_url = twc.Variable("orbited_url", default=None)
    topics = twc.Variable("topics", default=[])

    stomp_host = twc.Param(default=config.get('stomp_host', 'localhost'))
    stomp_port = twc.Param(default=config.get('stomp_port', 61613))
    stomp_user = twc.Param(default=config.get('stomp_user', 'guest'))
    stomp_pass = twc.Param(default=config.get('stomp_pass', 'guest'))

    def prepare(self):
        if not self.orbited_url:
            self.orbited_url = '%s://%s:%s' % (
                self.orbited_scheme, self.orbited_host, self.orbited_port)
        super(StompWidget, self).prepare()    
        self.onmessageframe = defaultdict(str) # {topic: 'js callbacks'}
        for callback in self.callbacks:
            if len(moksha.utils.livewidgets[callback]):
                cbs = ''
                if callback == 'onmessageframe':
                    for topic in moksha.utils.livewidgets[callback]:
                        self.topics.append(topic)
                        for cb in moksha.utils.livewidgets[callback][topic]:
                            self.onmessageframe[topic] += '%s;' % str(cb)
                else:
                    for cb in moksha.utils.livewidgets[callback]:
                        if isinstance(cb, (twc.js_callback, js_function)):
                            cbs += '$(%s);' % str(cb)
                        else:
                            cbs += str(cb)
                if cbs:
                    setattr(self, callback, cbs)

        if self.notify:
            moksha_notify.register_resources()
            openmsg = "Moksha live socket connected"
            self.onopen = twc.js_callback(
                'function() { $.jGrowl("%s") }' % openmsg)
            errormsg = "Moksha Live Socket Error: "
            self.onerror = twc.js_callback(
                'function(error) { $.jGrowl("%s" + error) }' % errormsg)
            errorframemsg = "Error frame received from Moksha Socket: "
            self.onerrorframe = twc.js_callback(
                'function(f) { $.jGrowl("%s" + f) }' % errorframemsg)
            closemsg = "Moksha Socket Closed"
            self.onclose = twc.js_callback(
                'function(c) { $.jGrowl("%s") }' % closemsg)
