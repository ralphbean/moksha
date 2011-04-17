## -*- coding: utf-8 -*-
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
:mod:`moksha.apps.menus.widgets` - Moksha Menu Widgets
======================================================

This is a powerful component to build easily a multilevel tree menu or a
contextual menu (right click) in an intuitive way.

This module contains ToscaWidgets for the `mbMenu jQuery Plugin
<http://plugins.jquery.com/project/mbMenu>`_, which was developed by Matteo
Bicocchi. © 2002-2008 Open Lab srl, Matteo Bicocchi. GPL licensed.

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

import tw2.core as twc
from tw2.jquery import jquery_js
from tw2.jquery.base import jQuery

from moksha.lib.helpers import when_ready

modname = __name__

jquery_mbmenu_js = twc.JSLink(modname=modname,
                              filename='static/mbMenu.js')
jquery_mbmenu_min_js = twc.JSLink(modname=modname,
                                  filename='static/mbMenu.min.js')

mbmenu_css_1 = twc.CSSLink(modname=modname, filename='static/css/menu1.css',
                           media='screen')
mbmenu_css = twc.CSSLink(modname=modname, filename='static/css/menu.css',
                         media='screen')
mbmenu_resources = twc.DirLink(modname=modname, filename='static/images',
                               media='screen')

# TODO -- this should be broken out into tw2.jqplugins.mbmenu
class MokshaMenuBase(twc.Widget):
    template = "mako:moksha.apps.menus.templates.mbmenu"
    resources = [
        jquery_js, jquery_mbmenu_min_js, mbmenu_css_1,
        mbmenu_resources,
    ]

    rootMenuSelector = 'rootVoices'
    menuSelector = 'menuContainer'
    callback = '/apps/menu'
    iconPath = '/resources/moksha.apps.menus.widgets/static/images/'
    additionalData = ""
    menus = []
    menuWidth = 200
    openOnRight =  False
    hasImages = True
    fadeTime = 200
    fadeInTime = 100
    fadeOutTime = 100
    adjustLeft = 2
    adjustTop = 10
    opacity = 0.95
    shadow = True
    overflow = 2
    effect = 'fade'
    minZindex = 'auto'


class MokshaMenu(MokshaMenuBase):
    def prepare(self):
        super(MokshaMenu, self).prepare()

        if not self.id:
            raise Exception("MokshaMenu must have an id!")
        if not self.callback:
            raise Exception("Must provide a callback URL!")

        menus = []
        for menu in self.menus:
            menus.append((menu.lower().replace(' ', ''), menu))
        self.menus = menus

        self.add_call(when_ready(jQuery('.%s' % self.id).buildMenu({
                'template': self.callback,
                'additionalData': self.additionalData,
                'menuWidth': self.menuWidth,
                'openOnRight': self.openOnRight,
                'rootMenuSelector': ".%s" % self.rootMenuSelector,
                'menuSelector': ".%s" % self.menuSelector,
                'iconPath': self.iconPath,
                'hasImages': self.hasImages,
                'fadeTime': self.fadeTime,
                'fadeInTime': self.fadeInTime,
                'fadeOutTime': self.fadeOutTime,
                'adjustLeft': self.adjustLeft,
                'adjustTop': self.adjustTop,
                'opacity': self.opacity,
                'shadow': self.shadow,
                'minZindex': self.minZindex,
                })))


class MokshaContextualMenu(MokshaMenuBase):

    def prepare(self):
        super(MokshaContextualMenu, self).prepare()

        if not self.id:
            raise Exception("MokshaMenu must have an id!")
        if not self.callback:
            raise Exception("Must provide a callback URL!")

        menus = []
        for menu in self.menus:
            menus.append((menu.lower().replace(' ', ''), menu))
        self.menus = menus

        self.add_call(jQuery(twc.JSSymbol(src='document')).buildContextualMenu({
                'template': self.callback,
                'menuWidth': self.menuWidth,
                'rootMenuSelector': ".%s" % self.rootMenuSelector,
                'menuSelector': ".%s" % self.menuSelector,
                'iconPath': self.iconPath,
                'hasImages': self.hasImages,
                'fadeTime': self.fadeTime,
                'fadeInTime': self.fadeInTime,
                'fadeOutTime': self.fadeOutTime,
                'adjustLeft': self.adjustLeft,
                'adjustTop': self.adjustTop,
                'opacity': self.opacity,
                'shadow': self.shadow,
                'effect': self.effect,
                'minZindex': self.minZindex
                }))
