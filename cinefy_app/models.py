from django.db import models
import uuid

# Create your models here.
class Movie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)

    def __str__(self):
        return str(self.id)
    