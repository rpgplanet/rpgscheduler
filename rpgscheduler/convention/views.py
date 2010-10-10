from django.http import Http404
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponseBadRequest

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ellaschedule.models import Event, Occurrence

from rpgscheduler.convention.events import create_event
from rpgscheduler.convention.forms import EventForm, AgendaForm

def home(request, template='con/home.html', max_occurrences=10, oldest_occurence_interval=None):
    """
    Display home page. By default, HP gets list of all upcoming ocurrences
    of all non-private events.

    ``max_occurrences``
        Limit how many courrences HP gets

    ``oldest_occurrence_interval``
        How long to look back

    Context Variables:

    ``calendar``
        The Calendar object designated by the ``calendar_slug``.
    """
    if oldest_occurence_interval is None:
        oldest_occurence_interval = timedelta(days=30)

    occurrences = Occurrence.objects.select_related().filter(
        start__lte = datetime.now(),
        end__gte = datetime.now() - oldest_occurence_interval
    )[0:max_occurrences]

    return render_to_response(template, {
        "ocurrences": occurrences,
    }, context_instance=RequestContext(request))


@login_required
def new(request, template='con/new.html'):
    if request.method == "POST":
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = create_event(author=request.user, **event_form.cleaned_data)
            return HttpResponseRedirect(reverse("con:event-profile", kwargs={
                'event_id' : event.pk
            }))

    else:
        event_form = EventForm()
    return render_to_response(template, {
        'event_form' : event_form
    }, context_instance=RequestContext(request))

def profile(request, event_id, template='con/event.html'):
    event = get_object_or_404(Event, pk=event_id)

    return render_to_response(template, {
        'event' : event,
        'agendas' : event.get_structured_agenda(),
    }, context_instance=RequestContext(request))


@login_required
def agenda_edit(request, event_id, agenda_id=None, template='con/agenda_edit.html'):
    event = get_object_or_404(Event, pk=event_id)
    agenda = None
    if agenda_id:
        agenda = get_object_or_404(Event, pk=agenda_id)

#    if request.user not in event.user_authors:
#        raise Http403()

    standard_attributes = ['title', 'start', 'end', 'place']

    if request.method == "POST":
        #TODO: Verify that agenda is inside event time
        #TODO: Author might not be user / request.user
        agenda_form = AgendaForm(request.POST)
        if agenda_form.is_valid():
            if request.POST.get('save', None):
                if not agenda:
                    create_event(
                        parent = event,
                        author = request.user,
                        # public = event.is_public
                        **agenda_form.cleaned_data
                    )
                else:
                    for attr in standard_attributes:
                        setattr(agenda, attr, agenda_form.cleaned_data[attr])
                    agenda.djangomarkup_description = agenda_form.cleaned_data['description']
                    agenda.save()

                return HttpResponseRedirect(reverse('con:agenda-edit', kwargs={'event_id' : event.pk}))
            
            elif request.POST.get('delete', None):
                agenda.delete()
                return HttpResponseRedirect(reverse('con:agenda-edit', kwargs={'event_id' : event.pk}))
            
            else:
                return HttpResponseBadRequest("Action name not recognized")

    elif agenda_id:
        agenda_form = AgendaForm(initial={
            'title' : agenda.title,
            'place' : agenda.place,
            'start' : agenda.start.strftime('%Y-%m-%d %H:%M'),
            'end' : agenda.end.strftime('%Y-%m-%d %H:%M'),
            'description' : agenda.djangomarkup_description
        })
    else:
        agenda_form = AgendaForm()

    return render_to_response(template, {
        'agenda_form' : agenda_form,
        'event' : event,
        'agenda' : agenda,
        'agendas' : event.get_structured_agenda()
    }, context_instance=RequestContext(request))
