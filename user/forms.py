from django import forms
from django.forms import ValidationError

from user.models import Profile


class ProfileForm(forms.ModelForm):
    def clean_max_distance(self,):
        clean_data = self.clean()
        min_distance = clean_data.get('min_distance')
        max_distance = clean_data.get('max_distance')
        if min_distance > max_distance:
            raise ValidationError('min_distance > max_distance')
        return max_distance

    def clean_max_dating_age(self,):
        clean_data = self.clean()
        min_dating_age = clean_data.get('min_dating_age')
        max_dating_age = clean_data.get('max_dating_age')
        if min_dating_age > max_dating_age:
            raise ValidationError('min_dating_age > max_dating_age')
        return max_dating_age

    class Meta:
        model = Profile
        fields = "__all__"


