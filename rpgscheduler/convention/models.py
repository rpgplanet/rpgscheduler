from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from ellaschedule.models import Event

class Proposal(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("event"))
    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"))
    cancelled = models.BooleanField(_("cancelled"), default=False)

class ProposalVote(models.Model):
    user = models.ForeignKey(User)
    proposal = models.ForeignKey(Proposal)
    
    class Meta:
        unique_together = ("user", "proposal")

