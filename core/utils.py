from django.db import models
from django_lifecycle import LifecycleModelMixin

class BaseModel(models.Model,LifecycleModelMixin):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
            ('Deleted', 'Deleted')
        ],
        default='Active'
    )

    class Meta:
        abstract = True
