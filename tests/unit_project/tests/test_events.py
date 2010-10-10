# -*- coding: utf-8 -*-
from djangosanetesting.cases import DatabaseTestCase

from datetime import datetime, timedelta

from ellaschedule.models import Event

from rpgcommon.user.user import create_user

from rpgscheduler.convention.events import create_event

class TestEventsCreation(DatabaseTestCase):
    def setUp(self):
        super(TestEventsCreation, self).setUp()
        self.now = datetime.now()
        self.user = create_user(u"Andrej Tokarčík", "xxx", "tester@example.com")

    def create_default_event(self):
        self.event = create_event(
            title = u"PragoCon",
            start = self.now,
            end = self.now + timedelta(hours=1),
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

class TestAgenda(DatabaseTestCase):
    def setUp(self):
        super(TestAgenda, self).setUp()
        self.user = create_user(u"Andrej Tokarčík", "xxx", "tester@example.com")
        self.holger = create_user(u"Holger", "xxx", "holger@example.com")

        self.now = datetime.now()

        self.event = create_event(
            title = u"PragoCon",
            start = self.now,
            end = self.now + timedelta(hours=1),
            description = u'''
= Cool event =

Sluníčkový event s unicodem.

""Frikulínskej"", as in """角色扮演游戏""".
''',
            is_public = True,
            facebook_publish = False,
            author = self.user
        )

        self.agenda_one = create_event(
            title = u"Úvod do Poezie",
            start = self.now,
            end = self.now + timedelta(hours=1),
            description = u'''
= Úvod do poezie =

S Olgou. Bude tam hodně znaků.
''',
            is_public = True,
            facebook_publish = False,
            author = self.holger,
            parent = self.event,
            place = u'Místnost 1'
        )

    def test_agenda_retrieved(self):
        self.assert_equals(1, len(self.event.get_agenda()))

    def test_agenda_structured_properly(self):
        start_time = self.now.time()
        start_time = start_time.replace(second=0, microsecond=0)

        expected = [
            {
                'date' : self.now.date(),
                'places' : [u'Místnost 1'],
                'agenda' : {
                    start_time : [self.agenda_one]
                }
            }
        ]

        result = self.event.get_structured_agenda()

        self.assert_equals(len(expected), len(result))
        self.assert_equals(expected[0]['date'], result[0]['date'])
        self.assert_equals(expected[0]['places'], result[0]['places'])
        self.assert_equals(expected[0]['agenda'][start_time], result[0]['agenda'][start_time])

    def test_deleting_agenda_do_not_delete_event(self):
        self.agenda_one.delete()

        self.assert_equals(1, Event.objects.count())
        