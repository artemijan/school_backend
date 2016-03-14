from .views import RegistrationView
from django.conf.urls import include, url
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^activate/complete/$',
        RedirectView.as_view(url='/#/activation/complete'),
        name='registration_activation_complete'),
    url(r'^register/$', RegistrationView.as_view(),
        name='registration_register'),
    url(r'^register/complete/$',
        RedirectView.as_view(url='/#/registration/complete'),
        name='registration_complete'),
    url(r'^register/closed/$',
        RedirectView.as_view(url='/#/registration/closed'),
        name='registration_disallowed'),
    url(r'', include('registration.auth_urls')),
]
