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
:mod:`moksha.api.widgets.amqp` - An AMQP driven live Moksha socket
==================================================================

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

import moksha
import moksha.utils

from tg import config
import tw2.core as twc
from tw2.jquery import jquery_js
from paste.deploy.converters import asbool

from moksha.api.widgets.orbited import orbited_host, orbited_port, orbited_url
from moksha.lib.helpers import defaultdict, listify
from moksha.widgets.moksha_js import moksha_js, moksha_extension_points_js
from moksha.widgets.notify import moksha_notify
from moksha.widgets.json import jquery_json_js

from widgets import (
    kamaloka_qpid_js, kamaloka_protocol_0_10_js, kamaloka_protocol_js,
)

def amqp_subscribe(topic):
    """ Return a javascript callback that subscribes to a given topic,
        or a list of topics.
    """
    sub = """
        moksha.debug("Subscribing to the '%(topic)s' topic");
        moksha_amqp_queue.subscribe({
            exchange: 'amq.topic',
            remote_queue: moksha_amqp_remote_queue,
            binding_key: '%(topic)s',
            callback: moksha_amqp_on_message,
        });
    """
    return ''.join([sub % {'topic': t} for t in listify(topic)])


def amqp_unsubscribe(topic):
    """ Return a javascript callback that unsubscribes to a given topic,
        or a list of topics.
    """
    return ""
    # TODO:
    #sub = "stomp.unsubscribe('%s');"
    #if isinstance(topic, list):
    #    sub = ''.join([sub % t for t in topic])
    #else:
    #    sub = sub % topic
    #return sub


class AMQPSocket(twc.Widget):
    callbacks = ['onconnectedframe', 'onmessageframe']
    resources = [
        jquery_js, jquery_json_js, moksha_js, moksha_extension_points_js,
        kamaloka_protocol_js, kamaloka_protocol_0_10_js, kamaloka_qpid_js,
    ]
    onconnectedframe = twc.Param('', default='')
    onmessageframe = twc.Param('', default='')
    send_hook = twc.Param('', default='')
    recieve_hook = twc.Param('', default='')

    template = "mako:moksha.api.widgets.amqp.templates.amqp"

    # TODO -- what is this?
    hidden = twc.Param("TODO -- what is this?", default=True)

    notify = twc.Param(
        '', default=asbool(config.get('moksha.socket.notify', False)))
    orbited_host = twc.Param(
        '', default=config.get('orbited_host', 'localhost'))
    orbited_port = twc.Param(
        '', default=config.get('orbited_port', 9000))
    orbited_scheme = twc.Param(
        '', default=config.get('orbited_scheme', 'http'))
    amqp_broker_host = twc.Param(
        '', default=config.get('amqp_broker_host', 'localhost'))
    amqp_broker_port = twc.Param(
        '', default=config.get('amqp_broker_port', 5672))
    amqp_broker_user = twc.Param(
        '', default=config.get('amqp_broker_user', 'guest'))
    amqp_broker_pass = twc.Param(
        '', default=config.get('amqp_broker_pass', 'guest'))

    def prepare(self):
        super(AMQPSocket, self).prepare()
        self.orbited_url = '%s://%s:%s' % (
            self.orbited_scheme, self.orbited_host, self.orbited_port)
        self.topics = []
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
                        if isinstance(cb, (twc.js_callback, twc.js_function)):
                            cbs += '$(%s);' % str(cb)
                        else:
                            cbs += str(cb)
                if cbs:
                    setattr(self, callback, cbs)
