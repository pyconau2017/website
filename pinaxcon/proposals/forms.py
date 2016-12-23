from django import forms

from pinaxcon import widgets

from .models import TalkProposal, TutorialProposal, MiniconfProposal
from .models import SysAdminProposal, WriteTheDocsProposal, WootconfProposal
from .models import KernelProposal, OpenRadioProposal, SecurityProposal
from .models import GamesProposal, TestingProposal, LawProposal, OpenHardwareProposal
from .models import KnowledgeProposal

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

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }


class TutorialProposalForm(ProposalForm):

    class Meta:
        model = TutorialProposal
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

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }


class MiniconfProposalForm(ProposalForm):

    class Meta:
        model = MiniconfProposal
        fields = [
            "title",
            "abstract",
            "private_abstract",
            "technical_requirements",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class SysAdminProposalForm(ProposalForm):

    class Meta:
        model = SysAdminProposal
        fields = [
            "title",
            "talk_format",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class WriteTheDocsProposalForm(ProposalForm):

    class Meta:
        model = WriteTheDocsProposal
        fields = [
            "title",
            "talk_format",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class RadioProposalForm(ProposalForm):

    class Meta:
        model = OpenRadioProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class KernelProposalForm(ProposalForm):

    class Meta:
        model = KernelProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class WootconfProposalForm(ProposalForm):

    class Meta:
        model = WootconfProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class SecurityProposalForm(ProposalForm):

    class Meta:
        model = SecurityProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class GamesProposalForm(ProposalForm):

    class Meta:
        model = GamesProposal
        fields = [
            "title",
            "talk_format",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class TestingProposalForm(ProposalForm):

    class Meta:
        model = TestingProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class KnowledgeProposalForm(ProposalForm):

    class Meta:
        model = KnowledgeProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class LawProposalForm(ProposalForm):

    class Meta:
        model = LawProposal
        fields = [
            "title",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }

class OpenHardwareProposalForm(ProposalForm):

    class Meta:
        model = OpenHardwareProposal
        fields = [
            "title",
            "talk_format",
            "target_audience",  
            "abstract",
            "private_abstract",
            "technical_requirements",
            "project",
            "project_url",
            "recording_release",
            "materials_release",
        ]

        widgets = {
            "abstract" : widgets.AceMarkdownEditor(),
            "private_abstract" : widgets.AceMarkdownEditor(),
            "technical_requirements" : widgets.AceMarkdownEditor(),
        }
