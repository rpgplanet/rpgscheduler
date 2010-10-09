# -*- coding: utf-8 -*-
from djangosanetesting.cases import DatabaseTestCase

from datetime import datetime, timedelta

from rpgcommon.user.user import create_user

from rpgscheduler.convention.events import create_event

class TestEventsCreation(DatabaseTestCase):
    def setUp(self):
        super(TestEventsCreation, self).setUp()
        self.user = create_user(u"Andrej Tokarčík", "xxx", "tester@example.com")

    def create_default_event(self):
        self.event = create_event(
            title = u"PragoCon",
            start = datetime.now(),
            end = datetime.now() + timedelta(hours=1),
            description = u'''
= Cool event =

Sluníčkový event s unicodem.

""Frikulínskej"", as in """角色扮演游戏""".
''',
            is_public = True,
            facebook_publish = False,
            author = self.user
        )

    def test_event_created_with_markup(self):
        self.create_default_event()
        self.assert_equals(self.event.description, u"<h1>Cool event</h1><p>Sluníčkový event s unicodem.</p><p><em>Frikulínskej</em>, as in <strong>角色扮演游戏</strong>.</p>")

    def test_event_created_with_single_ocurrence(self):
        self.create_default_event()

        self.assert_equals(1, len(self.event.get_occurrences(self.event.start, self.event.end)))

    def test_event_created_with_durating_ocurrence(self):
        self.create_default_event()

        self.assert_equals(self.event.start, self.event.get_occurrence(self.event.start).start)
