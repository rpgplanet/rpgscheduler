from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponseBadRequest

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ella.core.models import Author
from ellaschedule.models import Event, Occurrence
from esus.phorum.forms import TableCreationForm

from rpgscheduler.convention.events import create_event
from rpgscheduler.convention.comments import create_table
from rpgscheduler.convention.forms import EventForm, AgendaForm, ProposalCreationForm, ProposalVotingForm
from rpgscheduler.convention.models import Proposal, ProposalVote

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
def occurrence_proposal(request, event_id, template="con/occurrence_proposal.html"):
    event = get_object_or_404(Event, pk=event_id)
    proposals = Proposal.objects.filter(event=event)
    
    proposal_creation_form = None
    proposal_voting_form = None
    
    if request.method == "POST":
        if 'vote' in request.POST:
            proposal_voting_form = ProposalVotingForm(proposals=proposals, post=request.POST)
            
            if proposal_voting_form.is_valid():
                ProposalVote.objects.filter(user=request.user, proposal__in=proposals).delete()
                
                for pk in proposal_voting_form.cleaned_data['votes']:
                    ProposalVote.objects.create(
                        user = request.user,
                        proposal = Proposal.objects.get(pk=pk, event=event)
                    )

                return HttpResponseRedirect(reverse("con:event-occurrence-proposal", kwargs={
                    'event_id' : event.pk
                }))
                
            
        elif 'create_proposal' in request.POST:
            proposal_creation_form = ProposalCreationForm(request.POST)
            
            if proposal_creation_form.is_valid():
                
                Proposal.objects.create(
                    start = proposal_creation_form.cleaned_data['start'],
                    end = proposal_creation_form.cleaned_data['end'],
                    event = event
                )
                
                return HttpResponseRedirect(reverse("con:event-occurrence-proposal", kwargs={
                    'event_id' : event.pk
                }))
        else:
            return HttpResponseBadRequest()
    
    if not proposal_voting_form:
        proposal_voting_form = ProposalVotingForm(proposals=proposals, initial={'votes' : [str(p.proposal.pk) for p in ProposalVote.objects.select_related('proposal').filter(user=request.user, proposal__in=proposals)]})
        
    if not proposal_creation_form:
        proposal_creation_form = ProposalCreationForm()
    
    return render_to_response(template, {
        'event' : event,
        'proposals' : proposals,
        'proposal_voting_form' : proposal_voting_form, 
        'proposal_creation_form' : proposal_creation_form,
        
    }, context_instance=RequestContext(request))


@login_required
def events_personal(request, template='con/list.html'):
    """
    Show personal events.
    Personal events = those I have founded or I am attending to.
    """
    events = Event.objects.filter(
        authors = Author.objects.filter(user=request.user)
    )

    return render_to_response(template, {
        'events' : events,
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


def comments_create(request, event_id, template='con/comments/new.html'):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        table_form = TableCreationForm(request.POST)
        if table_form.is_valid():
            table, category = create_table(
                event = event,
                owner = request.user,
                **table_form.cleaned_data
            )
            return HttpResponseRedirect(reverse('esus-phorum-table', kwargs={
                'category' : category.slug,
                'table' : table.slug,
            }))
    else:
        table_form = TableCreationForm()


    return render_to_response(template, {
        'event' : event,
        'table_form' : table_form,
    }, context_instance=RequestContext(request))
