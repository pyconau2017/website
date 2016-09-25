from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

from django.contrib import admin

import symposion.views


urlpatterns = [
    #url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/", include("account.urls")),

    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),

    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    #url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),

    url(r"^teams/", include("symposion.teams.urls")),

    url(r"^boxes/", include("pinax.boxes.urls")),

    url(r'^cms/', include(wagtailadmin_urls)),

    # Wiki
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern()),

    # Default catch-all for wagtail pages.
    url(r'^', include(wagtail_urls)),

    # Matches *NOTHING* -- remove once site_tree is fixed
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),



    # Required by registrasion
#    url(r'^register/', include('registrasion.urls')),
#    url(r'^nested_admin/', include('nested_admin.urls')),

    # Demo payment gateway and related features
#    url(r"^register/pinaxcon/", include("pinaxcon.registrasion.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
