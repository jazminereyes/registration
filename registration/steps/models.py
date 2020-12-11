from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

# Create your models here.
class UserState(TimeStampedModel):
    step = models.IntegerField(
        _('Step'),
        default=1
    )

    is_finished = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
