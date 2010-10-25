from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from ella.core.models import Category

from esus.phorum.models import Table
from rpgscheduler.convention.categories import get_event_category

def create_table(event, owner, title, description):

    # every event get it's own category inside events category
    category = Category.objects.get_or_create(
        site = Site.objects.get_current(),
        title = event.title,
        slug = slugify(event.title),
        tree_path = "%s/%s" % (get_event_category(), slugify(title)),
        tree_parent = get_event_category(),
        description = event.description
    )[0]

    table = Table.objects.create(
        category = category,
        title = title,
        slug = slugify(title),
        description = description,
        owner = owner
    )

    return (table, category)


def create_comment():
    pass