# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.forms import (
    Form, ValidationError,
    IntegerField, CharField, DateTimeField, BooleanField, ChoiceField, MultipleChoiceField,
    Textarea, HiddenInput, CheckboxSelectMultiple,
)

availability_choices = (
    ("s", u"Vyberu níže"),
    ("n", u"Dohodnu s přáteli"),
)

class EventForm(Form):
    title = CharField(label=u"Název", max_length=255)
    date_available = ChoiceField(label=u"Termín", choices = availability_choices)
    start = DateTimeField(label=u"Začátek", input_formats=['%Y-%m-%d %H:%M'], initial=lambda:datetime.now().strftime('%Y-%m-%d %H:%M'))
    end = DateTimeField(label=u"Konec", input_formats=['%Y-%m-%d %H:%M'], initial=lambda:(datetime.now()+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'))
    description = CharField(label=u"Popis", widget=Textarea(), initial=u"""
== Popis akce ==

Můžete použí standardní Czechtile prvky, jako ""kurzívu"".

Ozvláštněte to jak můžete :o)
    """)
    place = CharField(label=u"Místo konání", max_length=255, required=False)
    is_public = BooleanField(required=False)
    facebook_publish = BooleanField(required=False)

    
    def clean_date_available(self):
        data = self.cleaned_data['date_available']
        if data == "s":
            data = True
        else:
            data = False
        return data
    
    def clean(self):
        date_available = self.cleaned_data.get('date_available', None)
        
        if date_available:
            start = self.cleaned_data.get('start', None)
            end = self.cleaned_data.get('end', None)
    
            if start and end and start >= end:
                raise ValidationError(u"Akce musí skončit až po svém začátku")
            
            return self.cleaned_data
        else:
            self.cleaned_data['start'] = None
            self.cleaned_data['end'] = None
            
            return self.cleaned_data

class AgendaForm(EventForm):
    pass

class ProposalCreationForm(Form):
    start = DateTimeField(label=u"Začátek", input_formats=['%Y-%m-%d %H:%M'], initial=lambda:datetime.now().strftime('%Y-%m-%d %H:%M'))
    end = DateTimeField(label=u"Konec", input_formats=['%Y-%m-%d %H:%M'], initial=lambda:(datetime.now()+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'))

class ProposalVotingForm(Form):
    def __init__(self, proposals, post=None, *args, **kwargs):

        self.base_fields['votes'] = MultipleChoiceField(
            required = False,
            choices = [(unicode(p.pk), "%s - %s" % (p.start.strftime('%Y-%m-%d %H:%M'), p.end.strftime('%Y-%m-%d %H:%M'))) for p in proposals],
            widget = CheckboxSelectMultiple(),
        )
        
        super(ProposalVotingForm, self).__init__(post, *args, **kwargs)
        