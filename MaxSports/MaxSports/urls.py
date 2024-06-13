"""
URL configuration for MaxSports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from Admin_side_app import urls
from product_app import urls
from category_app import urls
from order_app import urls
from coupons_app import urls
from banner_app import urls
from index_app import urls
from accounts import urls
from user_side import urls
from cart_app import urls
from payment import urls
from offers import urls
from wallet import urls
from visitors import urls

# from django.utils.functional import curry
# from django.views.defaults import permission_denied


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("index_app.urls")),
    path("", include("Admin_side_app.urls")),
    path("", include("user_side.urls")),
    path("", include("category_app.urls")),
    path("", include("banner_app.urls")),
    path("", include("order_app.urls")),
    path("", include("coupons_app.urls")),
    path("", include("product_app.urls")),
    path("", include("accounts.urls")),
    path("", include("cart_app.urls")),
    path("", include("payment.urls")),
    path("", include("offers.urls")),
    path("", include("wallet.urls")),
    path("", include("visitors.urls")),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "index_app.views.my_custom_404_view"
# handler403 = curry(permission_denied, template_name='user/403.html')
