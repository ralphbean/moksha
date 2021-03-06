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

from paste.deploy.converters import asbool
from tg import config

from pylons import tmpl_context

import tw.api
import tw2.core as twc


class TW1ContextAwareWidget(tw.api.Widget):
    '''Inherit from this widget class if you want your widget
       to automatically get the pylons.tmpl_context in its dictionary
    '''

    def update_params(self, d):
        super(TW1ContextAwareWidget, self).update_params(d)
        d['tmpl_context'] = tmpl_context


class TW2ContextAwareWidget(twc.Widget):
    '''Inherit from this widget class if you want your widget
       to automatically get the pylons.tmpl_context in its dictionary
    '''

    tmpl_context = twc.Variable("A reference to the template context.")

    def prepare(self):
        super(TW2ContextAwareWidget, self).prepare()
        self.tmpl_context = tmpl_context


if asbool(config.get('moksha.use_tw2', False)):
    ContextAwareWidget = TW2ContextAwareWidget
else:
    ContextAwareWidget = TW1ContextAwareWidget
