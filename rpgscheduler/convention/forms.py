# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.forms import (
    Form, ValidationError,
    CharField, DateTimeField, Textarea, BooleanField
)


class EventForm(Form):
    title = CharField(label=u"Název", max_length=255)
    start = DateTimeField(label=u"Začátek", input_formats='%Y-%m-%d %H:%M', initial=datetime.now)
    end = DateTimeField(label=u"Konec", input_formats='%Y-%m-%d %H:%M', initial=lambda:datetime.now()+timedelta(hours=1))
    description = CharField(label=u"Popis", widget=Textarea(), initial=u"""
== Popis akce ==

Můžete použí standardní Czechtile prvky, jako ""kurzívu"".

Ozvláštněte to jak můžete :o)
    """)
    is_public = BooleanField(required=False)
    facebook_publish = BooleanField(required=False)


    def clean(self):
        start = self.cleaned_data.get('start', None)
        end = self.cleaned_data.get('end', None)
        if start and end:
            if start >= end:
                raise ValidationError(u"Akce musí skončit po začátku")

        return self.cleaned_data