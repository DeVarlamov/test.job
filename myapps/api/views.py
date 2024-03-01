from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from api.permissions import IsAdmin
from djoser.views import UserViewSet
from product.models import Product, Lesson, Group, Purchase
from users.models import User
from .serializers import (
    ProductSerializer,
    LessonListSerializer,
    GroupListSerializer,
    UserSerializer,
    ProductCreateSerializer,
    lessonCreateSerializer,
    PurchaseSerializer
    )


class UsersViewSet(UserViewSet):

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    filter_backends = (SearchFilter,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProductSerializer
        return ProductCreateSerializer

    @staticmethod
    def adding_products(add_serializer, model, request, products_id):
        """Кастомный метод добавления и удаления продукта."""
        user = request.user
        data = {'buyer': user.id, 'product': products_id}
        serializer = add_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @action(
        detail=True, methods=['post'], permission_classes=(IsAuthenticated,)
    )
    def shopfavorite(self, request, pk):
        return self.adding_products(PurchaseSerializer, Purchase, request, pk)

    @shopfavorite.mapping.delete
    def deliteshops(self, request, pk):
        get_object_or_404(Purchase, buyer=request.user, product=pk).delete()
        return Response(
            {'detail': 'Успешно удаленный продукт'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=['get'])
    def my_lesson(self, request):
        purchases = Purchase.objects.filter(buyer=request.user)
        products = [purchase.product for purchase in purchases]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return LessonListSerializer
        return lessonCreateSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer
    permission_classes = (AllowAny,)
