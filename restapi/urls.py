from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from .views import PetView, PetImageCreateView


urlpatterns = [
    path(r'pets', PetView.as_view()),
    path(r'pets/<int:pk>/photo', PetImageCreateView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
