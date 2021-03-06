from django.db import models

from pagemanager.permissions import get_published_status_name, \
    get_public_visibility_name


class PageManager(models.Manager):
    """
    A manager that provides some convenience methods to find objects based on
    status, visibility and draft copy mode.
    """
    def published(self):
        """ Returns all published items."""
        return self.get_query_set().filter(
            status=get_published_status_name()
        )

    def unpublished(self):
        """ Returns all unpublished objects."""
        return self.get_query_set().exclude(
            status=get_published_status_name()
        )

    def public(self):
        """ Returns all publicly visible items."""
        return self.get_query_set().filter(
            visibility=get_public_visibility_name()
        )

    def private(self):
        """ Returns all private items."""
        return self.get_query_set().exclude(
            visibility=get_public_visibility_name()
        )

    def draft_copies(self):
        """ Returns all draft copies."""
        return self.get_query_set().exclude(
            copy_of__exact=None
        )

    def generate_materialized_paths(self):
        """
        Warms up the ``materialized_path`` model field in all Pages.
        Returns the number of pages that were updated.
        """
        counter = 0
        for page in self.get_query_set().all():
            materialized_path = page.get_materialized_path()
            self.model.objects.filter(pk=page.pk).update(
                materialized_path=materialized_path
            )
            counter += 1
        return counter