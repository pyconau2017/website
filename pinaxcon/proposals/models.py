from django.db import models

from symposion.proposals.models import ProposalBase


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
        help_text="I allow Linux Australia to release any recordings of "
        "presentations covered by this proposal, under the <a "
        "href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> "
        "Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"
    )

    materials_release = models.BooleanField(
        default=True,
        help_text="I allow Linux Australia to release any other material "
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

class TutorialProposal(Proposal):

    class Meta:
        verbose_name = "tutorial proposal"

class MiniconfProposal(ProposalBase):

    class Meta:
        verbose_name = "miniconf proposal"
