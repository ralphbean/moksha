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
from tw2.jquery import jquery_js
from moksha.lib.helpers import eval_app_config, ConfigWrapper
from tg import config

from moksha.lib.helpers import eval_app_config, ConfigWrapper

class AppListWidget(twc.Widget):
    template = 'mako:moksha.api.widgets.containers.templates.layout_applist'
    category = twc.Param()

    def prepare(self):
        super(AppListWidget, self).prepare()

        # ignore categories that don't exist
        c = self.category
        if isinstance(c, basestring):
            found = False
            for cat in self.layout:
                if cat['label'] == c:
                    self.category = cat
                    found = True
                    break

            # ignore categories that don't exist
            if not found:
                self.category = None

applist_widget = AppListWidget(id='applist');

class DashboardContainer(twc.Widget):
    template = 'mako:moksha.api.widgets.containers.templates.dashboardcontainer'
    config_key = twc.Param(default=None)
    layout = twc.Variable()
    applist_widget = twc.Param(default=applist_widget)
    engine_name = 'mako'

    def prepare(self):
        super(DashboardContainer, self).prepare()
        layout = eval_app_config(config.get(self.config_key, "None"))

        if not layout:
            if isinstance(self.layout, basestring):
                layout = eval_app_config(self.layout)
            else:
                layout = self.layout

        # Filter out any None's in the layout which signify apps which are
        # not allowed to run with the current session's authorization level
        self.layout = ConfigWrapper.process_wrappers(layout, d)
