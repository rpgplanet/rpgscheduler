from django.http import Http404
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ellaschedule.models import Event, Occurrence

from rpgscheduler.convention.events import create_event
from rpgscheduler.convention.forms import EventForm

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
                "year" : event.start.strftime("%Y"),
                "month" : event.start.strftime("%m"),
                "day" : event.start.strftime("%d"),
                "slug" : event.slug,
            }))

    else:
        event_form = EventForm()
    return render_to_response(template, {
        'event_form' : event_form
    }, context_instance=RequestContext(request))

def profile(request, year, month, day, slug, template='con/event.html'):
    try:
        day = datetime(year=int(year), month=int(month), day=int(day))
    except ValueError:
        raise Http404()
    
    events = Event.objects.filter(
        start__gte = day,
        end__lt = (day + timedelta(days=1)),
        slug = slug
    )
    
    if len(events) < 1:
        raise Http404()
    elif len(events) > 1:
        raise ValueError("Multiple event results for %s" % str(day))

    event = events[0]

    return render_to_response(template, {
        'event' : event,
    }, context_instance=RequestContext(request))

