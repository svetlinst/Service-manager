from django.db import models
from django.db.models import Q


class ActiveQuerySet(models.QuerySet):
    def delete(self):
        self.update(active=False)


class ActiveManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        return self.model.objects.filter(active=True)

    def all_with_inactive(self):
        return self.model.objects.filter(Q(active=True) | Q(active=False))

    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)
