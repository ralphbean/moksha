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

from tw2.jqplugins.flot import FlotWidget
from moksha.api.widgets import LiveWidget

class LiveFlotWidget(LiveWidget, FlotWidget):
    """ A live graphing widget """
    topic = None
    onmessage = '$.plot($("#${id}"),json[0]["data"],json[0]["options"])'
    height = '250px'
    width = '390px'

    def prepare(self):
        # IMHO this constitutes a bug in tw2.core upstream.
        # Widgets should automatically gather and combine the resources of their
        # parent widget classes.  You have to do it manually, which sucks.
        self.resources += LiveWidget.resources + FlotWidget.resources
        super(LiveFlotWidget, self).prepare()
