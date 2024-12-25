from django.urls import path
from .views import faq_view

urlpatterns = [
    # path("", faq_view, name="faq_home"),
    path('', faq_view, name='faq'),
]
