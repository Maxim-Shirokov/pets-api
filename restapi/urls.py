from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from .views import PetView, PetImageCreateView


urlpatterns = [
    path(r'pets', PetView.as_view(), name='pets'),
    path(r'pets/<str:pk>/photo', PetImageCreateView.as_view(), name='add_pet_photo'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
