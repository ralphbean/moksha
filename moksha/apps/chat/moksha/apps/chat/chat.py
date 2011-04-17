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

import tw2.core as twc
from tw2.jquery import jquery_js

from moksha.api.widgets.orbited import orbited_js

irc2_js = twc.JSLink(filename='static/irc2.js',
                 modname=__name__)

willowchat_js = twc.JSLink(filename='static/willowchat.js',
                       modname=__name__)

gui_js = twc.JSLink(filename='static/gui.js',
                modname=__name__)

willowchat_css = twc.CSSLink(filename='static/style.css', modname=__name__)

static_dir = twc.DirLink(filename='static', modname=__name__)


class LiveChatWidget(twc.Widget):
    name = 'Chat'
    template = 'mako:moksha.apps.chat.templates.chatwidget'
    bootstrap = twc.Param(default=twc.JSLink(link='/apps/chat/bootstrap'))
    visible = False
    resources = [static_dir]


class LiveChatFrameWidget(twc.Widget):
    template = 'mako:moksha.apps.chat.templates.chat'
    resources= [jquery_js, orbited_js, willowchat_js, irc2_js, gui_js,
                willowchat_css, static_dir]
