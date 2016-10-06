import models

from django import forms


class YesNoField(forms.TypedChoiceField):

    def __init__(self, *a, **k):
        super(YesNoField, self).__init__(
            *a,
            coerce=lambda x: x =='True',
            choices=((False, 'No'), (True, 'Yes')),
            widget=forms.RadioSelect,
            **k
        )


class ProfileForm(forms.ModelForm):
    ''' A form for requesting badge and profile information. '''

    class Meta:
        model = models.AttendeeProfile
        exclude = ['attendee']
        field_classes = {
            "of_legal_age" : YesNoField,
        }
        widgets = {
            "past_lca" : forms.widgets.CheckboxSelectMultiple(),
        }


    class Media:
        js = ("lca2017/js/profile_form.js", )
