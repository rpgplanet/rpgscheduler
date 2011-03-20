from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify

from ella.core.models import Author, Category

from ellaschedule.models import Event

def create_event(title, start, end, description, is_public, facebook_publish, author, calendar=None, parent=None, place=None, date_available=None):

    try:
        root_category = Category.objects.get(
            site = Site.objects.get_current(),
            tree_parent = None
        )
    except Category.DoesNotExist:
        root_category = Category.objects.create(
            site = Site.objects.get_current(),
            tree_path = "",
            tree_parent = None,
            title = author.username,
            slug = slugify(author.username)
        )



    ella_author = Author.objects.get_or_create(
            user = author,
            name = author.username,
            slug = slugify(author.username)
    )[0]

    opts = {}
    if calendar:
        opts['calendar'] = calendar

    # we're not interested in (mili) seconds in events...and they lead to feaky things
    if start:
        start = start.replace(second=0, microsecond=0)
    if end:
        end = end.replace(second=0, microsecond=0)

    event = Event.objects.create(
        title = title,
        slug = slugify(title),
        start = start,
        end = end,
        category = root_category,
        creator = author,
        parent_event = parent,
        place = place,
        **opts
    )

    event.djangomarkup_description = description
    event.authors.add(ella_author)
    event.save()

    # if is_public add to public calendar
    # if facebook_publish send using fb api

    return event