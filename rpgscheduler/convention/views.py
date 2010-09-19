from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from ellaschedule.models import Occurrence


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
