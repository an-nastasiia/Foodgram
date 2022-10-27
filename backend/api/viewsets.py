from rest_framework import mixins, viewsets


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    '''Базовый вьюсет с возможностью создания и удаления объекта.'''

    pass


class CreateListDestroyViewSet(CreateDestroyViewSet,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    '''Базовый вьюсет для создания, удаления и получения списка объектов.'''

    pass
