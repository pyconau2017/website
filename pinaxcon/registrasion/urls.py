from django.conf.urls import *

import views

urlpatterns = [
    "pinaxcon.registrasion.views",
    url(r"^demopay/([0-9]+)/([A-Z0-9]+)$", views.demopay, name="demopay"),
]
