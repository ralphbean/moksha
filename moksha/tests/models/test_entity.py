# -*- coding: utf-8 -*-
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

#"""Test Moksha's Entity/Fact model"""

#from datetime import datetime
#from nose.tools import eq_, assert_true
#from sqlalchemy import *
#from moksha.tests.models import ModelTest

#from moksha.apps.knowledge.model import DBSession, Entity, Fact, with_characteristic, metadata
#
#class TestEntity(ModelTest):
#    """Test case for the Entity model."""
#
#    klass = Entity
#    attrs = dict(name=u'lmacken')
#
#    def setup(self):
#        super(TestEntity, self).setup()
#        self.obj[u'firstname'] = u'Luke'
#        self.obj[u'lastname'] = u'Macken'
#        self.obj[u'age'] = 24
#        self.obj[u'dob'] = datetime(1984, 11, 02)
#        self.obj[u'l33t'] = True
#        self.obj[u'json'] = {'foo':'bar'}
#
#    def test_entity_creation_name(self):
#        eq_(self.obj.name, u'lmacken')
#
#    def test_fact_types(self):
#        DBSession.add(self.obj)
#        DBSession.flush()
#        me = DBSession.query(Entity).filter_by(name=u'lmacken').one()
#        eq_(me[u'lastname'], u'Macken')
#        eq_(me[u'age'], 24)
#        eq_(me[u'dob'], datetime(1984, 11, 2))
#        eq_(me[u'l33t'], True)
#
#    def test_getting_by_name(self):
#        """ Entities should be fetchable by their name """
#        DBSession.add(self.obj)
#        lmacken = Entity.by_name(u'lmacken')
#        eq_(lmacken, self.obj)
#
#    def test_filter_by_name(self):
#        DBSession.add(self.obj)
#        me = DBSession.query(Entity).filter_by(name=u'lmacken').one()
#        eq_(me.name, u'lmacken')
#        eq_(me[u'firstname'], u'Luke')
#
#    def test_query_by_fact(self):
#        """ Query entities by facts """
#        DBSession.add(self.obj)
#        assert DBSession.query(Entity).filter(
#                Entity.facts.any(
#                    and_(Fact.key == u'l33t',
#                         Fact.value == True))).first()
#
#    def test_query_with_characteristic(self):
#        """ Query entities based on facts using with_characteristic """
#        DBSession.add(self.obj)
#        assert (DBSession.query(Entity).
#                filter(or_(Entity.facts.any(
#                    with_characteristic(u'dob', datetime(1984, 11, 02))),
#                    not_(Entity.facts.any(Fact.key == u'l33t'))))).first()
#
#    def test_query_facts_by_characteristic(self):
#        """ Query facts by certain characteristics """
#        DBSession.add(self.obj)
#        assert (DBSession.query(Fact).
#                filter(with_characteristic(u'l33t', True))).one()
#
#    def test_child_entities(self):
#        child = Entity(u'child1')
#        DBSession.add(child)
#        self.obj.append(child)
#        DBSession.flush()
#        me = Entity.by_name(u'lmacken')
#        assert_true('child1' in me.children)
#        eq_(self.obj.children['child1'].parent, me)
#
#    def test_entity_json_fact(self):
#        me = Entity.by_name(u'lmacken')
#        eq_(me[u'json'], {'foo': 'bar'})
#
#    """
#    TODO: add hooks that send AMQP messages?
#    Or, do this i
#    def test_hooks(self):
#        from moksha.hook import Hook, MokshaHookMapperExtension
#        from moksha.model import model
#        insert = update = delete = False
#
#        class MyHook(Hook):
#            def after_insert(self, instance):
#                insert = True
#            def after_update(self, instance):
#                update = True
#            def after_delete(self, instance):
#                delete = True
#
#        model.moksha_mapper_extension.hooks['after_insert'].append(MyHook())
#
#        # create a new entity
#        something = Entity(u'something')
#        DBSession.add(something)
#        DBSession.flush()
#        assert insert
#    """
