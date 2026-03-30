from django.db import models

from .utils import build_unique_slug


class AutoSlugMixin(models.Model):
    slug_source_field = "name"

    class Meta:
        abstract = True

    def get_slug_source(self):
        return getattr(self, self.slug_source_field)

    def ensure_slug(self):
        if getattr(self, "slug", ""):
            return
        self.slug = build_unique_slug(
            self.__class__,
            self.get_slug_source(),
            instance=self,
        )


class ReferenceCodeMixin(models.Model):
    reference_prefix = ""

    class Meta:
        abstract = True

    def ensure_reference_code(self, field_name):
        if getattr(self, field_name):
            return False
        if not self.pk or not getattr(self, "created_at", None):
            return False
        setattr(
            self,
            field_name,
            f"{self.reference_prefix}-{self.created_at:%Y%m%d}-{self.pk}",
        )
        return True
