from collections import namedtuple
from datetime import datetime as datetime_notz
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone

from registrasion.models import inventory as inv
from registrasion.models import conditions as cond
from symposion import proposals


class Command(BaseCommand):
    help = 'Populates the inventory with the PyConAu17 inventory model'

    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true',
                            dest='debug', default=False,
                            help='Sets dates and capacities such that testing is easier.')

    def handle(self, *args, **options):

        self.debug = options.get('debug')

        kinds = []
        for i in ("talk", "Tutorial"):
            kinds.append(proposals.models.ProposalKind.objects.get(name=i))
        self.main_conference_proposals = kinds

        self.populate_groups()
        self.populate_inventory()
        self.populate_restrictions()
        self.populate_discounts()

    def populate_groups(self):
        self.group_team = self.find_or_make(
            Group,
            ("name", ),
            name="Conference organisers",
        )
        self.group_volunteers = self.find_or_make(
            Group,
            ("name", ),
            name="Conference volunteers",
        )
        self.group_unpublish = self.find_or_make(
            Group,
            ("name", ),
            name="Can see unpublished products",
        )

    def populate_inventory(self):
        # Categories

        self.conf_ticket = self.find_or_make(
            inv.Category,
            ("name",),
            name="Conference Ticket (Sat 5th - Sun 6th)",
            description="Each type of conference ticket has different included products. "
                        "For details of what products are included, see our "
                        "<a href=\"/attend/\">registration details page</a>.",
            required=True,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=1,
            order=40,
        )
        self.specialist_day = self.find_or_make(
            inv.Category,
            ("name",),
            name="Specialist Day (Fri 4th)",
            description="Our specialist day consists of <a href=\"/program/specialist-tracks/\">four tracks.</a>",
            required=False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            order=30,
        )
        self.tute_ticket_morn = self.find_or_make(
            inv.Category,
            ("name",),
            name="Morning Tutorial Ticket (Thurs 3rd)",
            description="Each of our <a href=\"/program/tutorials/\">four tutorials</a> has its own ticket.",
            required=False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=2,
            order=10,
        )
        self.tute_ticket_aft = self.find_or_make(
            inv.Category,
            ("name",),
            name="Afternoon Tutorial Ticket (Thurs 3rd)",
            description="Each of our <a href=\"/program/tutorials/\">four tutorials</a> has its own ticket",
            required=False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=2,
            order=20,
        )
        self.sprint_ticket = self.find_or_make(
            inv.Category,
            ("name",),
            name="Sprint Ticket (Mon 7th - Tue 8th)",
            description="Sprints are a day where you get to work with other members of the community. "
                        "This is a great opportunity to spend some in-person time with members of the community. "
                        "Bring your laptop, we'll supply the WiFi. You get to decide what you work on. ",
            required=False,
            render_type=inv.Category.RENDER_TYPE_CHECKBOX,
            limit_per_user=2,
            order=60,
        )

        self.child_care = self.find_or_make(
            inv.Category,
            ("name",),
            name="Child Care",
            description="Child care will be offered for the full program day on the specialist track and main conference days (Friday, Saturday and Sunday). "
                        "This child care will be on-site at the MCEC, and run by qualified child care workers. "
                        "If you register for child care, we will contact you for needed details about each child.",
            required=False,
            render_type=inv.Category.RENDER_TYPE_QUANTITY,
            order=70,
        )

        self.t_shirt = self.find_or_make(
            inv.Category,
            ("name",),
            name="T-Shirt",
            description="If you'd like something physical to remember the conference by, select your <a href=\"/attend/t-shirts/\">t-shirt</a>.",
            required=False,
            render_type=inv.Category.RENDER_TYPE_ITEM_QUANTITY,
            order=100,
        )

        # Conf Tickets
        self.ticket_supporter = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Supporter",
            price=Decimal("900.00"),
            reservation_duration=hours(24),
            order=1,
        )
        self.ticket_professional = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Professional",
            price=Decimal("660.00"),
            reservation_duration=hours(24),
            order=10,
        )
        self.ticket_enthusiast = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Enthusiast",
            price=Decimal("360.00"),
            reservation_duration=hours(24),
            order=20,
        )
        self.ticket_student = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Student",
            price=Decimal("60.00"),
            reservation_duration=hours(24),
            order=30,
        )
        self.ticket_specialist_only = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Specialist Day Only (Fri 4th ONLY)",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=40,
        )
        self.ticket_speaker = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Speaker",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=50,
        )
        self.ticket_media = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Media",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=60,
        )
        self.ticket_sponsor = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Sponsor",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=70,
        )
        self.ticket_team = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Conference Organiser",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=80,
        )
        self.ticket_volunteer = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Conference Volunteer",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=90,
        )

        self.ticket_djangogirls = self.find_or_make(
            inv.Product,
            ("name", "category",),
            name="DjangoGirls",
            category=self.conf_ticket,
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=100)

        self.ticket_soldout = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="SOLD OUT",
            price=Decimal("00.00"),
            description="This ticket does NOT give you access to the conference.",
            reservation_duration=hours(24),
            order=110)

        # Specialist day
        self.ticket_specialist_inclusion = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.specialist_day,
            name="Specialist Day Inclusion",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=40,
        )
        self.ticket_specialist_addon = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.specialist_day,
            name="Specialist Day Add-on",
            price=Decimal("75.00"),
            reservation_duration=hours(24),
            order=40,
        )

        # Tutorial tickets
        self.tutorial_a = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket_morn,
            name="Build Tooling, Rita Garcia",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        self.tutorial_b = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket_morn,
            name="Python 101, Anthony Briggs",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        self.tutorial_c = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket_aft,
            name="Bayesian inference & machine learning, Dr Edward Schofield",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        self.tutorial_d = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket_aft,
            name="Practical testing with pytest, Brianna Laugher",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        # Sprint tickets
        self.sprint_ticket_monday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.sprint_ticket,
            name="Monday",
            price=Decimal("5.00"),
            reservation_duration=hours(24),
            order=10)

        self.sprint_ticket_tuesday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.sprint_ticket,
            name="Tuesday",
            price=Decimal("5.00"),
            reservation_duration=hours(24),
            order=20)

        # Child care
        childcare_price = Decimal("30.00")

        self.childcare_friday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.child_care,
            name="Friday",
            price=childcare_price,
            reservation_duration=hours(24),
            order=10)

        self.childcare_saturday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.child_care,
            name="Saturday",
            price=childcare_price,
            reservation_duration=hours(24),
            order=10)

        self.childcare_sunday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.child_care,
            name="Sunday",
            price=childcare_price,
            reservation_duration=hours(24),
            order=10)

        # Shirts
        ShirtGroup = namedtuple("ShirtGroup", ("prefix", "sizes"))
        shirt_names = {
            "mens": ShirtGroup(
                "Men's/Straight Cut Size",
                ("S", "M", "L", "XL", "2XL", "3XL", "5XL"),
            ),
            "womens_classic": ShirtGroup(
                "Women's Classic Fit",
                ("XS", "S", "M", "L", "XL", "2XL"),
            ),
            "womens_semi": ShirtGroup(
                "Women's Semi-Fitted",
                ("S", "M", "L", "XL", "2XL"),
            ),
        }

        self.shirts = {}
        order = 0
        for name, group in shirt_names.items():
            self.shirts[name] = {}
            prefix = group.prefix
            for size in group.sizes:
                product_name = "%s %s" % (prefix, size)
                order += 10
                self.shirts[name][size] = self.find_or_make(
                    inv.Product,
                    ("name", "category",),
                    name=product_name,
                    category=self.t_shirt,
                    price=Decimal("25.00"),
                    reservation_duration=hours(1),
                    order=order,
                )

    def populate_restrictions(self):

        # Hide the products that will eventually need a voucher
        hide_voucher_products = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="Can see hidden products",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        hide_voucher_products.group.set([self.group_unpublish])
        hide_voucher_products.products.set([
            self.ticket_media,
            self.ticket_sponsor,
            self.ticket_djangogirls,
        ])

        # Set limits.
        tshirt_deadline = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Tshirt deadline",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            end_time=datetime(year=2017, month=7, day=3),
        )
        self.shirt_products = []
        for name in self.shirts:
            for size in self.shirts[name]:
                self.shirt_products.append(self.shirts[name][size])

        tshirt_deadline.products.set(self.shirt_products)

        public_mainconf_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Public main conf cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=550,
        )
        public_mainconf_cap.products.set([
            self.ticket_supporter,
            self.ticket_professional,
            self.ticket_enthusiast,
            self.ticket_student,
            self.ticket_specialist_only,
        ])

        private_ticket_cap = 600

        non_public_ticket_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Non-public main conf cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=private_ticket_cap,
        )
        non_public_ticket_cap.products.set([
            self.ticket_speaker,
            self.ticket_sponsor,
            self.ticket_media,
            self.ticket_team,
            self.ticket_volunteer,
        ])

        sold_out_available = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Enable SOLD OUT tickets.",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
            start_time=datetime(year=2018, month=1, day=1),
        )
        sold_out_available.products.set([
            self.ticket_soldout,
        ])

        specialist_day_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Specialist day cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=private_ticket_cap,
        )

        specialist_day_cap.products.set([
            self.ticket_specialist_inclusion,
            self.ticket_specialist_addon,
            self.ticket_specialist_only,
        ])

        tutorial_capacity = 60

        tutorial_a_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Tutorial A cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=tutorial_capacity,
        )
        tutorial_a_cap.products.set([self.tutorial_a])

        tutorial_b_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Tutorial B cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=tutorial_capacity,
        )
        tutorial_b_cap.products.set([self.tutorial_b])

        tutorial_c_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Tutorial C cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=tutorial_capacity,
        )
        tutorial_c_cap.products.set([self.tutorial_c])

        tutorial_d_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Tutorial D cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=tutorial_capacity,
        )
        tutorial_d_cap.products.set([self.tutorial_d])

        sprint_capacity = 80

        sprint_monday_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Monday sprint cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=sprint_capacity,
        )
        sprint_monday_cap.products.set([self.sprint_ticket_monday])

        sprint_tuesday_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description",),
            description="Tuesday sprint cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=sprint_capacity,
        )
        sprint_tuesday_cap.products.set([self.sprint_ticket_tuesday])

        childcare_cap = 20

        childcare_friday_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Friday childcare cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=childcare_cap,
        )
        childcare_friday_cap.products.set([self.childcare_friday])

        childcare_saturday_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Saturday childcare cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=childcare_cap,
        )
        childcare_saturday_cap.products.set([self.childcare_saturday])

        childcare_sunday_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Sunday childcare cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=childcare_cap,
        )
        childcare_sunday_cap.products.set([self.childcare_sunday])

        # Volunteer tickets are for volunteers only
        volunteers = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="Volunteer tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        volunteers.group.set([self.group_volunteers])
        volunteers.products.set([
            self.ticket_volunteer,
        ])

        # Team tickets are for team members only
        team = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="Team tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        team.group.set([self.group_team])
        team.products.set([
            self.ticket_team,
        ])

        # Speaker tickets are for primary speakers only
        speaker_tickets = self.find_or_make(
            cond.SpeakerFlag,
            ("description", ),
            description="Speaker tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
            is_presenter=True,
            is_copresenter=False,
        )
        speaker_tickets.proposal_kind.set(self.main_conference_proposals)
        speaker_tickets.products.set([self.ticket_speaker, ])

        specialist_day_included_dep = self.find_or_make(
            cond.ProductFlag,
            ("description",),
            description="Specialist day inclusion only for professional tickets.",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )

        specialist_day_included_dep.enabling_products.set([
            self.ticket_supporter,
            self.ticket_professional,
            self.ticket_speaker,
            self.ticket_media,
        ])

        specialist_day_included_dep.products.set([
            self.ticket_specialist_inclusion,
        ])

        specialist_day_addon_dep = self.find_or_make(
            cond.ProductFlag,
            ("description",),
            description="Specialist day add-on only for certain tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )

        specialist_day_addon_dep.enabling_products.set([
            self.ticket_enthusiast,
            self.ticket_student,
        ])

        specialist_day_addon_dep.products.set([
            self.ticket_specialist_addon,
        ])

        extras_dep = self.find_or_make(
            cond.CategoryFlag,
            ("description",),
            description="extras are only available for conference attendees",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
            enabling_category=self.conf_ticket,
        )

        extras_dep.products.set([
            self.childcare_friday, self.childcare_saturday, self.childcare_sunday,
            self.sprint_ticket_monday, self.sprint_ticket_tuesday,
            self.tutorial_a, self.tutorial_b, self.tutorial_c, self.tutorial_d,
        ] +
            self.shirt_products,
        )

    def populate_discounts(self):

        def add_early_birds(discount):
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_sponsor,
                percentage=Decimal("50.00"),
                quantity=1,  # Per user
            )
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_professional,
                price=Decimal("165.00"),
                quantity=1,  # Per user
            )
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_enthusiast,
                price=Decimal("110.00"),
                quantity=1,  # Per user
            )

        def free_category(parent_discount, category, quantity=1):
            self.find_or_make(
                cond.DiscountForCategory,
                ("discount", "category",),
                discount=parent_discount,
                category=category,
                percentage=Decimal("100.00"),
                quantity=quantity,
            )

        # Early Bird Discount (general public)
        early_bird = self.find_or_make(
            cond.TimeOrStockLimitDiscount,
            ("description", ),
            description="Early Bird",
            end_time=datetime(year=2017, month=6, day=14),
            limit=100,  # Across all users
        )
        add_early_birds(early_bird)

        # Professional-Like ticket inclusions
        ticket_prolike_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Complimentary for ticket holder (Professional-level)",
        )
        ticket_prolike_inclusions.enabling_products.set([
            self.ticket_supporter,
            self.ticket_professional,
            self.ticket_media,
            self.ticket_sponsor,
            self.ticket_speaker,
        ])
        free_category(ticket_prolike_inclusions, self.t_shirt)

        # Enthusiast ticket inclusions
        ticket_enthusiast_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Complimentary for ticket holder (Enthusiast-level)",
        )
        ticket_enthusiast_inclusions.enabling_products.set([
            self.ticket_enthusiast,
        ])
        free_category(ticket_enthusiast_inclusions, self.t_shirt)

        # Team & volunteer ticket inclusions
        ticket_staff_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Complimentary for ticket holder (staff/volunteer)",
        )
        ticket_staff_inclusions.enabling_products.set([
            self.ticket_team,
            self.ticket_volunteer,
        ])

        # Team & volunteer t-shirts, regardless of ticket type
        staff_t_shirts = self.find_or_make(
            cond.GroupMemberDiscount,
            ("description", ),
            description="T-shirts complimentary for staff and volunteers",
        )
        staff_t_shirts.group.set([
            self.group_team,
            self.group_volunteers,
        ])
        free_category(staff_t_shirts, self.t_shirt, quantity=5)

    def find_or_make(self, model, search_keys, **k):
        ''' Either makes or finds an object of type _model_, with the given
        kwargs.

        Arguments:
            search_keys ([str, ...]): A sequence of keys that are used to search
            for an existing version in the database. The remaining arguments are
            only used when creating a new object.
        '''

        try:
            keys = dict((key, k[key]) for key in search_keys)
            a = model.objects.get(**keys)
            self.stdout.write("FOUND  : " + str(keys))
            model.objects.filter(id=a.id).update(**k)
            a.refresh_from_db()
            return a
        except ObjectDoesNotExist:
            a = model.objects.create(**k)
            self.stdout.write("CREATED: " + str(k))
            return a


def hours(n):
    return timedelta(hours=n)


def datetime(year, month, day):
    return datetime_notz(year, month, day, tzinfo=timezone.utc)
