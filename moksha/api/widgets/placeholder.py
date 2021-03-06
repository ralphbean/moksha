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

from tg import config
from paste.deploy.converters import asbool

import tw.api
import tw2.core as twc


class TW1Placeholder(tw.api.Widget):
    hidden = twc.Param(default=True)
    template = "mako:moksha.api.widgets.templates.placeholder"


class TW2Placeholder(twc.Widget):
    hidden = twc.Param(default=True)
    template = "mako:moksha.api.widgets.templates.placeholder"


if asbool(config.get('moksha.use_tw2', False)):
    Placeholder = TW2Placeholder
else:
    Placeholder = TW1Placeholder
