from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify

from ella.core.models import Category

def get_root_category():
    if getattr(Category, 'cached_root_category', None):
        return Category.cached_root_category

    title = getattr(settings, "CON_ROOT_CATEGORY_TITLE", "Conventions"),
    description = getattr(settings, "CON_ROOT_CATEGORY_DESCRIPTION", "Description"),

    try:
        return Category.objects.get(
            site = Site.objects.get_current(),
            tree_path = ""
        )
    except Category.DoesNotExist:
        return Category.objects.create(
            site = Site.objects.get_current(),
            tree_path = "",
            title = title,
            slug = slugify(title),
            tree_parent = None,
            description = description
        )

def get_event_category():
    if getattr(Category, 'cached_event_category', None):
        return Category.cached_event_category

    title = getattr(settings, "CON_EVENT_CATEGORY_TITLE", "Conventions"),
    description = getattr(settings, "CON_EVENT_CATEGORY_DESCRIPTION", "Description"),

    try:
        return Category.objects.get(
            site = Site.objects.get_current(),
            tree_path = slugify(title),
        )
    except Category.DoesNotExist:
        return Category.objects.create(
            site = Site.objects.get_current(),
            title = title,
            slug = slugify(title),
            tree_path = slugify(title),
            tree_parent = get_root_category(),
            description = description
        )
