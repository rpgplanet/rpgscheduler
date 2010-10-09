from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify

from ella.core.models import Author, Category

from ellaschedule.models import Event

def create_event(title, start, end, description, is_public, facebook_publish, author, calendar=None):

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



    author = Author.objects.get_or_create(
            user = author,
            name = author.username,
            slug = slugify(author.username)
    )[0]

    opts = {}
    if calendar:
        opts['calendar'] = calendar

    event = Event.objects.create(
        title = title,
        slug = slugify(title),
        start = start,
        end = end,
        category = root_category,
        **opts
    )

    event.djangomarkup_description = description
    event.authors.add(author)
    event.save()

    # if is_public add to public calendar
    # if facebook_publish send using fb api

    return event