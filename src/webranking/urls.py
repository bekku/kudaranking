from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_v905sjd98/', admin.site.urls),
    path('',include('ranking.urls')),
    path('top/', TemplateView.as_view(template_name='top.html'), name='top'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('auth/', include('allauth.urls')),

    path('chat/',include('chat.urls')),
    path('social_django', include('social_django.urls', namespace='social')),
]
