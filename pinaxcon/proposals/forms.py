from django import forms

from .models import TalkProposal


class ProposalForm(forms.ModelForm):

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value


class TalkProposalForm(ProposalForm):

    class Meta:
        model = TalkProposal
        fields = [
            "title",
            "target_audience",
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "video_url",
            "recording_release",
            "materials_release",
        ]
