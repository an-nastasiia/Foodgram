from rest_framework import mixins, viewsets


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    '''Base viewset for creating and destroying objects.'''

    pass


class CreateListDestroyViewSet(CreateDestroyViewSet,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    '''Base viewset for getting list, creating and destroying objects.'''

    pass
