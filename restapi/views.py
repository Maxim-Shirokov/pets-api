from distutils.util import strtobool

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import PetSerializer, PetAddPhotoSerializer
from .models import Pet, PetPhoto


NOT_FOUND_ERROR_MESSAGE = 'Pet with the matching ID was not found.'


class PetViewSet(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = PetSerializer

    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 20))
        offset = int(self.request.query_params.get('offset', 0))
        has_photos = self.request.query_params.get('has_photos')
        has_photos = strtobool(has_photos) if has_photos else None

        if has_photos is None:
            pets = Pet.objects.prefetch_related('photos')[offset:offset + limit]
        elif has_photos:
            pets = Pet.objects.filter(photos__isnull=False).prefetch_related('photos')[offset:offset + limit]
        else:
            pets = Pet.objects.exclude(photos__isnull=False)[offset:offset + limit]

        return pets

    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'count': count, 'item': serializer.data})

    def delete(self, request, **kwargs):
        ids = request.data.get('ids', [])
        count_deleted = 0
        errors = []
        for id in ids:
            try:
                instance = Pet.objects.get(pk=id)
                instance.delete()
                count_deleted += 1
            except Pet.DoesNotExist:
                error = {'id': id, 'error': NOT_FOUND_ERROR_MESSAGE}
                errors.append(error)
        return Response({'deleted': count_deleted, 'errors': errors})


class PetImageCreateView(generics.CreateAPIView):
    
    serializer_class = PetAddPhotoSerializer

    def create(self, request, *args, **kwargs):
        try:
            id = self.kwargs.get('pk')
            pet = Pet.objects.get(id=id)
        except Pet.DoesNotExist:
            return Response(data=NOT_FOUND_ERROR_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(pet=pet)
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
