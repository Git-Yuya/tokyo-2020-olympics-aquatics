from django.forms import ModelForm
from .models import SwimmingResult


class SwimmingResultForm(ModelForm):
    class Meta:
        model = SwimmingResult
        fields = ["sport", "event", "rank", "athletes", "team", "record"]
