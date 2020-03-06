from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet
# , MetadataViewset, IndexViewset, AttrsViewset

from django.conf.urls import url

import django_saml2_auth.views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)

# router.register(r'index', IndexViewset, basename='index')
# router.register(r'attrs', AttrsViewset, basename='attrs')
# router.register(r'metadata', MetadataViewset, basename='metadata')

urlpatterns = [
    # These are the SAML2 related URLs. You can change "^saml2_auth/" regex to
    # any path you want, like "^sso_auth/", "^sso_login/", etc. (required)
    url(r'^saml2_auth/', include('django_saml2_auth.urls')),

    # The following line will replace the default user login with SAML2 (optional)
    # If you want to specific the after-login-redirect-URL, use parameter "?next=/the/path/you/want"
    # with this view.
    url(r'^accounts/login/$', django_saml2_auth.views.signin),

    # The following line will replace the admin login with SAML2 (optional)
    # If you want to specific the after-login-redirect-URL, use parameter "?next=/the/path/you/want"
    # with this view.
    url(r'^admin/login/$', django_saml2_auth.views.signin),

    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
