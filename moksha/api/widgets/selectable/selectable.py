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

import tw2.core as twc
from tw2.jqplugins.ui.base import jquery_ui_js
from tw2.jquery.base import jQuery
from tw2.jquery import jquery_js
from uuid import uuid4


moksha_ui_selectable_js = twc.JSLink(
    modname='moksha', filename='public/javascript/ui/moksha.ui.selectable.js')

class Selectable(twc.Widget):
    template = 'mako:moksha.api.widgets.selectable.templates.selectable'
    resources = [jquery_js, jquery_ui_js, moksha_ui_selectable_js]
    content_id = twc.Variable()

    def prepare(self):
        super(Selectable, self).prepare()
        self.content_id = d.id + '-uuid' + str(uuid4())
        self.add_call(jQuery("#%s" % d.content_id).moksha_selectable())

