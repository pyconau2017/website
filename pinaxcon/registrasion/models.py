from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_countries.fields import CountryField
from registrasion import models as rego


@python_2_unicode_compatible
class PastEvent(models.Model):
    ''' This is populated in 0001_initial.py '''

    def __str__(self):
        return self.name

    year = models.IntegerField(unique=True,)
    name = models.CharField(max_length=255, unique=True,)


class AttendeeProfile(rego.AttendeeProfileBase):
    '''


Have you attended linux.conf.au before?

1999 (CALU, Melbourne)
2001 (Sydney)
2002 (Brisbane)
2003 (Perth)
2004 (Adelaide)
2005 (Canberra)
2006 (Dunedin)
2007 (Sydney)
2008 (Melbourne)
2009 (Hobart)
2010 (Wellington)
2011 (Brisbane)
2012 (Ballarat)
2013 (Canberra)
2014 (Perth)
2015 (Auckland)



Do you want?

Membership of Linux Australia. (read more)
The low traffic linux.conf.au 2016 announcement mailing list
The linux.conf.au 2016 attendees mailing listName
    '''

    @classmethod
    def name_field(cls):
        ''' This is used to pre-fill the attendee's name from the
        speaker profile. If it's None, that functionality is disabled. '''
        return "name"

    def invoice_recipient(self):

        lines = [
            self.name_per_invoice,
        ]

        if self.company:
            lines.append("C/- " + self.company)

        if self.address_line_1:
            lines.append(self.address_line_1)

        if self.address_line_2:
            lines.append(self.address_line_2)

        if self.address_suburb or self.address_postcode:
            lines.append("%s %s" % (
                self.address_suburb or "",
                self.address_postcode or "",
            ))

        if self.state:
            lines.append(self.state)

        if self.country:
            lines.append(self.country.name)

        return "\n".join(unicode(line) for line in lines)

    def clean(self):
        errors = []
        if self.country == "AU" and not self.state:
            errors.append(
                ("state", "Australians must list their state"),
            )

        if self.address_line_2 and not self.address_line_1:
            errors.append((
                "address_line_1",
                "Please fill in line 1 before filling line 2",
            ))

        if errors:
            raise ValidationError(dict(errors))

    def save(self):
        if not self.name_per_invoice:
            self.name_per_invoice = self.name
        super(AttendeeProfile, self).save()

    # Things that appear on badge
    name = models.CharField(
        verbose_name="Your name (for your conference nametag)",
        max_length=64,
        help_text="Your name, as you'd like it to appear on your badge. ",
    )
    company = models.CharField(
        max_length=64,
        help_text="The name of your company, as you'd like it on your badge",
        blank=True,
    )

    free_text_1 = models.CharField(
        max_length=64,
        verbose_name="Free text line 1",
        help_text="A line of free text that will appear on your badge. Use "
                  "this for your Twitter handle, IRC nick, your preferred "
                  "pronouns or anything else you'd like people to see on "
                  "your badge.",
        blank=True,
    )
    free_text_2 = models.CharField(
        max_length=64,
        verbose_name="Free text line 2",
        blank=True,
    )

    # Other important Information
    name_per_invoice = models.CharField(
        verbose_name="Your legal name (for invoicing purposes)",
        max_length=256,
        help_text="If your legal name is different to the name on your badge, "
                  "fill this in, and we'll put it on your invoice. Otherwise, "
                  "leave it blank.",
        blank=True,
        )

    address_line_1 = models.CharField(
        verbose_name="Address line 1",
        help_text="This address, if provided, will appear on your invoices.",
        max_length=1024,
        blank=True,
    )
    address_line_2 = models.CharField(
        verbose_name="Address line 2",
        max_length=1024,
        blank=True,
    )
    address_suburb = models.CharField(
        verbose_name="City/Town/Suburb",
        max_length=1024,
        blank=True,
    )
    address_postcode = models.CharField(
        verbose_name="Postal/Zip code",
        max_length=1024,
        blank=True,
    )
    country = CountryField(
        default="AU",
    )
    state = models.CharField(
        max_length=256,
        verbose_name="State/Territory/Province",
        blank=True,
    )

    of_legal_age = models.BooleanField(
        default=False,
        verbose_name="Are you over 18?",
        blank=True,
        help_text="Being under 18 will not stop you from attending the "
                  "conference. We need to know whether you are over 18 to "
                  "allow us to cater for you at venues that serve alcohol.",
    )
    dietary_restrictions = models.CharField(
        verbose_name="Food allergies, intolerances, or dietary restrictions",
        max_length=256,
        blank=True,
    )
    accessibility_requirements = models.CharField(
        verbose_name="Accessibility-related requirements",
        max_length=256,
        blank=True,
    )
    gender = models.CharField(
        help_text="Gender data will only be used for demographic purposes.",
        max_length=64,
        blank=True,
    )

    linux_australia = models.BooleanField(
        verbose_name="Linux Australia membership",
        help_text="Select this field to register for free "
                  "<a href='http://www.linux.org.au/'>Linux Australia</a> "
                  "membership.",
        blank=True,
    )

    lca_announce = models.BooleanField(
        verbose_name="Subscribe to PyCon Announce",
        help_text="Select to be subscribed to the low-traffic lca-announce "
                  "mailing list",
        blank=True,
    )

    past_lca = models.ManyToManyField(
        PastEvent,
        verbose_name="Which past PyCon Australia events have you attended?",
        blank=True,
    )
