from django.db import models

from symposion.proposals.models import ProposalBase
from symposion.conference.models import Section


class Proposal(ProposalBase):

    TARGET_USER = 1
    TARGET_BUSINESS = 2
    TARGET_COMMUNITY = 3
    TARGET_DEVELOPER = 4

    TARGET_AUIDENCES = [
        (TARGET_USER, "User"),
        (TARGET_BUSINESS, "Business"),
        (TARGET_COMMUNITY, "Community"),
        (TARGET_DEVELOPER, "Developer"),
    ]

    target_audience = models.IntegerField(choices=TARGET_AUIDENCES)

    recording_release = models.BooleanField(
        default=True,
        help_text="I allow PyCon Australia to release any recordings of "
        "presentations covered by this proposal, under the <a "
        "href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> "
        "Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"
    )

    materials_release = models.BooleanField(
        default=True,
        help_text="I allow PyCon Australia to release any other material "
        "(such as slides) from presentations covered by this proposal, under "
        "the <a "
        "href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> "
        "Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"
    )

    class Meta:
        abstract = True


class TalkProposal(Proposal):

    class Meta:
        verbose_name = "talk proposal"


class PyConAuProposal(Proposal):
    class Meta:
        verbose_name = "PyCon Australia talk proposal"

    area = models.ManyToManyField(
        Section,
        help_text="Please select the areas of the conference that you think your talk is applicable to. The paper committee may ask you to reconsider your desired areas.")

    LENGTH_SHORT = 1
    LENGTH_LONG = 2

    LENGTH_FORMATS = [
        (LENGTH_SHORT, "Short presentation (30mins)"),
        (LENGTH_LONG, "Long presentation (70mins)"),
    ]

    length = models.IntegerField(
        choices=LENGTH_FORMATS,
        help_text="Please select the desired length of your presentation. The paper committee may ask you to reconsider your desired length.")

    agreement = models.BooleanField(
        default=False,
        help_text="I agree to abide by our <a href=\"///cms/Terms_Conditions\">terms and conditions of attendance</a>, and "
        "that all parts of my presentation will adhere to our <a href=\"///cms/CoC\">Code of Conduct</a> "
    )


class TutorialProposal(Proposal):

    class Meta:
        verbose_name = "tutorial proposal"

class MiniconfProposal(ProposalBase):

    class Meta:
        verbose_name = "miniconf proposal"

class SysAdminProposal(Proposal):

    TYPE_SHORT_PRESENTATION = 1
    TYPE_LIGHTNING_TALK = 2
    
    TALK_FORMATS = [
        (TYPE_SHORT_PRESENTATION, "Short Presentation (15-25 min)"),
        (TYPE_LIGHTNING_TALK, "Lightning Talk (5-10 min)"),
    ]
    
    talk_format = models.IntegerField(choices=TALK_FORMATS,
        help_text="Please indicate your preferred talk length in the private abstract field below.")
    
    class Meta:
        verbose_name = "System Administration Miniconf Proposal"

class WriteTheDocsProposal(Proposal):

    TYPE_LONG_PRESENTATION = 1 
    TYPE_SHORT_PRESENTATION = 2
    
    TALK_FORMATS = [
        (TYPE_LONG_PRESENTATION, "Long Presentation (40 min)"),  
        (TYPE_SHORT_PRESENTATION, "Short Presentation (20 min)"),
    ]
    
    talk_format = models.IntegerField(choices=TALK_FORMATS)
    
    class Meta:
        verbose_name = "WriteThe Docs Miniconf Proposal"

class OpenRadioProposal(Proposal):

    class Meta:
        verbose_name = "OpenRadio Miniconf Proposal"

class WootconfProposal(Proposal):

    class Meta:
        verbose_name = "WOOTCONF Miniconf Proposal"

class KernelProposal(Proposal):

    class Meta:
        verbose_name = "Kernel Miniconf Proposal"

class SecurityProposal(Proposal):

    class Meta:
        verbose_name = "Security/Privacy Miniconf Proposal"

class GamesProposal(Proposal):

    TYPE_PRESENTATION = 1
    TYPE_DEMONSTRATION = 2
    TYPE_OTHER = 3

    TALK_FORMATS = [
        (TYPE_PRESENTATION, "Presentation"),
        (TYPE_DEMONSTRATION, "Demonstration"),
        (TYPE_OTHER, "Other"),
    ]
    
    talk_format = models.IntegerField(choices=TALK_FORMATS)
    
    class Meta:
        verbose_name = "Games and FOSS Miniconf Proposal"

class TestingProposal(Proposal):

    class Meta:
        verbose_name = "Testing/Automation Miniconf Proposal"

class KnowledgeProposal(Proposal):

    class Meta:
        verbose_name = "Open Knowledge Australia Miniconf Proposal"

class LawProposal(Proposal):

    class Meta:
        verbose_name = "Open Law and Policy Miniconf Proposal"

class OpenHardwareProposal(Proposal):

    TYPE_NORMAL_PRESENTATION = 1 
    TYPE_LIGHTNING_TALK = 2
    
    TALK_FORMATS = [
        (TYPE_NORMAL_PRESENTATION, "Presentation (20 min)"),  
        (TYPE_LIGHTNING_TALK, "Lightning Talk (5 min)"),
    ]
    
    talk_format = models.IntegerField(choices=TALK_FORMATS)
    
    class Meta:
        verbose_name = "Open Hardware Miniconf Proposal"
