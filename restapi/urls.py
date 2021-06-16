from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from .views import PetViewSet, PetImageCreateView


urlpatterns = [
    path(r'pets/', PetViewSet.as_view()),
    path(r'pets/<int:pk>/photo', PetImageCreateView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
