from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
import uuid

class BaseStampedModel(models.Model):
    created_at = models.DateTimeField( blank=False, null=False )
    # после создания объекта modified_at равен created_at
    modified_at = models.DateTimeField( blank=False, null=False )
    # main GUID
    GUID = models.CharField(max_length=100, blank=False, null=False)
    
    # этот класс - базовый и абстрактный, в db его включать не надо
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        n = timezone.now()
        # указать дату создания
        if not self.created_at:
            self.created_at = n
        if not self.GUID:
            self.GUID = uuid.uuid4().hex
        # указать дату изменения
        self.modified_at = n
        return super(BaseStampedModel, self).save(*args, **kwargs)