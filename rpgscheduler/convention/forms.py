# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.forms import (
    Form, ValidationError,
    IntegerField, CharField, DateTimeField, BooleanField,
    Textarea, HiddenInput
)


class EventForm(Form):
    title = CharField(label=u"Název", max_length=255)
    start = DateTimeField(label=u"Začátek", input_formats=['%Y-%m-%d %H:%M'], initial=lambda:datetime.now().strftime('%Y-%m-%d %H:%M'))
    end = DateTimeField(label=u"Konec", input_formats=['%Y-%m-%d %H:%M'], initial=lambda:(datetime.now()+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'))
    description = CharField(label=u"Popis", widget=Textarea(), initial=u"""
== Popis akce ==

Můžete použí standardní Czechtile prvky, jako ""kurzívu"".

Ozvláštněte to jak můžete :o)
    """)
    place = CharField(label=u"Místo konání", max_length=255)
    is_public = BooleanField(required=False)
    facebook_publish = BooleanField(required=False)


    def clean(self):
        start = self.cleaned_data.get('start', None)
        end = self.cleaned_data.get('end', None)

        if start and end and start >= end:
            raise ValidationError(u"Akce musí skončit až po svém začátku")
        
        return self.cleaned_data

class AgendaForm(EventForm):
    is_public = None
