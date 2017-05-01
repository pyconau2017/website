from collections import namedtuple
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from registrasion.models import inventory as inv
from registrasion.models import conditions as cond
from symposion import proposals


class Command(BaseCommand):
    help = 'Populates the inventory with the PyConAu17 inventory model'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

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
            name="Conference Ticket",
            description="Each type of conference ticket has different included products. "
                        "For details of what products are included, see our "
                        "[LINK]registration details page.[/LINK]",
            required=False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=1,
            order=1,
        )
        self.tute_ticket = self.find_or_make(
            inv.Category,
            ("name",),
            name="Tutorial Ticket",
            description="Each tutorial has it's own ticket.",
            required=False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=2,
            order=2,
        )

        self.sprint_ticket = self.find_or_make(
            inv.Category,
            ("name",),
            name="Sprint Ticket",
            description="A day of food, coffee and hacking",
            required=False,
            render_type=inv.Category.RENDER_TYPE_CHECKBOX,
            order=3,
        )

        self.child_care = self.find_or_make(
            inv.Category,
            ("name",),
            name="Child Care",
            description="On-site childcare is provided. Proof of vaccination is required. We'll ask you more details (e.g. food requirements) closer to the event.",
            required=False,
            render_type=inv.Category.RENDER_TYPE_QUANTITY,
            order=4,
        )

        self.t_shirt = self.find_or_make(
            inv.Category,
            ("name",),
            name="T-Shirt",
            description="Commemorative conference t-shirts",
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
            price=Decimal("1999.00"),
            reservation_duration=hours(24),
            order=1,
        )
        self.ticket_professional = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Professional",
            price=Decimal("999.00"),
            reservation_duration=hours(24),
            order=10,
        )
        self.ticket_enthusiast = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Enthusiast",
            price=Decimal("449.00"),
            reservation_duration=hours(24),
            order=20,
        )
        self.ticket_student = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Student",
            price=Decimal("160.00"),
            reservation_duration=hours(24),
            order=30,
        )
        self.ticket_miniconfs_mt = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Monday and Tuesday Only",
            price=Decimal("198.00"),
            reservation_duration=hours(24),
            order=40,
        )
        self.ticket_miniconfs_mon = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Monday Only",
            price=Decimal("99.00"),
            reservation_duration=hours(24),
            order=42,
        )
        self.ticket_miniconfs_tue = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.conf_ticket,
            name="Tuesday Only",
            price=Decimal("99.00"),
            reservation_duration=hours(24),
            order=44,
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

        # Tutorial tickets
        self.tutorial_a = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket,
            name="Tutorial A",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        self.tutorial_b = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket,
            name="Tutorial B",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        self.tutorial_c = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket,
            name="Tutorial C",
            price=Decimal("150.00"),
            reservation_duration=hours(24),
            order=10,
        )

        self.tutorial_a = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.tute_ticket,
            name="Tutorial D",
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
            price=Decimal("15.00"),
            reservation_duration=hours(24),
            order=10)

        self.sprint_ticket_tuesday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.sprint_ticket,
            name="Tuesday",
            price=Decimal("15.00"),
            reservation_duration=hours(24),
            order=20)

        # Child care
        self.childcare_friday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.child_care,
            name="Friday",
            price=Decimal("999.99"),
            reservation_duration=hours(24),
            order=10)

        self.childcare_saturday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.child_care,
            name="Saturday",
            price=Decimal("999.99"),
            reservation_duration=hours(24),
            order=10)

        self.childcare_sunday = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.child_care,
            name="Sunday",
            price=Decimal("999.99"),
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
        ])

        # Set limits.
        public_ticket_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Public ticket cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=450,
        )
        public_ticket_cap.products.set([
            self.ticket_supporter,
            self.ticket_professional,
            self.ticket_enthusiast,
            self.ticket_student,
        ])

        non_public_ticket_cap = self.find_or_make(
            cond.TimeOrStockLimitFlag,
            ("description", ),
            description="Non-public ticket cap",
            condition=cond.FlagBase.DISABLE_IF_FALSE,
            limit=450,
        )
        non_public_ticket_cap.products.set([
            self.ticket_speaker,
            self.ticket_sponsor,
            self.ticket_media,
            self.ticket_team,
            self.ticket_volunteer,
        ])

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

    def populate_discounts(self):

        def add_early_birds(discount):
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_sponsor,
                price=Decimal("150.00"),
                quantity=1,  # Per user
            )
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_professional,
                price=Decimal("150.00"),
                quantity=1,  # Per user
            )
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_enthusiast,
                price=Decimal("100.00"),
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
            end_time=datetime(year=2016, month=11, day=1),
            limit=165,  # Across all users
        )
        add_early_birds(early_bird)

        # Early bird rates for speakers
        speaker_ticket_discounts = self.find_or_make(
            cond.SpeakerDiscount,
            ("description", ),
            description="Speaker Ticket Discount",
            is_presenter=True,
            is_copresenter=True,
        )
        speaker_ticket_discounts.proposal_kind.set(
            self.main_conference_proposals,
        )
        add_early_birds(speaker_ticket_discounts)

        # Primary speaker gets a free speaker dinner ticket
        primary_speaker = self.find_or_make(
            cond.SpeakerDiscount,
            ("description", ),
            description="Complimentary for primary proposer",
            is_presenter=True,
            is_copresenter=False,
        )
        primary_speaker.proposal_kind.set(self.main_conference_proposals)

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

        # Student ticket inclusions
        ticket_student_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Complimentary for ticket holder (Student-level)",
        )
        ticket_student_inclusions.enabling_products.set([
            self.ticket_student,
        ])
        free_category(ticket_student_inclusions, self.t_shirt)

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
