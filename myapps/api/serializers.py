import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied

from users.models import ROLE_CHOICES, User
from product.models import Product, Lesson, Group, Purchase


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользовательской модели."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        )


class CreatorSerializer(serializers.ModelSerializer):
    """Сериализатор для имени и фамилии создателя продукта."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class GroupSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('name', 'students_count')

    def get_students_count(self, obj):
        return obj.students.count()


class ProductSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    groups = GroupSerializer(source='group_set', many=True)

    class Meta:
        model = Product
        fields = ('id', 'creator', 'name',
                  'start_date', 'price', 'groups')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.start_date > timezone.now():
            representation['start_date'] = instance.start_date.strftime(
                '%d-%m-%Y %H:%M')
            return representation
        else:
            return None


class ProductCreateSerializer(ProductSerializer):
    start_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M',
                                           input_formats=['%d-%m-%Y %H:%M'])

    class Meta(ProductSerializer.Meta):
        fields = ('name', 'start_date', 'price', 'student_counter')

    def validate_start_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Стартовое время не может быть"
                                              " меньше сегоднешнего дня.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_admin:
            raise PermissionDenied("Только учителя могут создавать продукты")

        validated_data['creator'] = user
        return Product.objects.create(**validated_data)



class LessonListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Lesson
        fields = ('product', 'name', 'video_link')


class lessonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('product', 'name', 'video_link')


class GroupListSerializer(serializers.ModelSerializer):
    students = CreatorSerializer(many=True)
    product = ProductSerializer()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('name', 'students_count')

    def get_students_count(self, obj):
        return obj.students.count()


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        buyer = data.get('buyer')
        user = self.context['request'].user

        if Purchase.objects.filter(product=product, buyer=buyer).exists():
            raise ValidationError("Вы уже приобрели этот продукт")

        if user.role != ROLE_CHOICES.TEACHER:
            raise ValidationError("Только учителя могут удалять продукты")

        return data

    def create(self, validated_data):
        product = validated_data['product']
        buyer = validated_data['buyer']

        groups = Group.objects.filter(product=product)

        if product.start_date <= timezone.now():
            for group in groups:
                if group.students.count() < product.student_counter:
                    group.students.add(buyer)
                    return super().create(validated_data)
        else:
            groups = sorted(groups, key=lambda x: x.students.count())
            min_students = min(group.students.count() for group in groups)
            max_students = max(group.students.count() for group in groups)

            for group in groups:
                if group.students.count() == min_students:
                    if group.students.count() < product.student_counter and (max_students - group.students.count()) <= 1:
                        group.students.add(buyer)
                        return super().create(validated_data)

            new_group = Group.objects.create(
                product=product, name=f"Группа {len(groups) + 1}")
            new_group.students.add(buyer)

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_name = instance.product.name
        group_name = Group.objects.filter(
            product=instance.product, students=instance.buyer).first().name
        representation['user'] = instance.buyer.username
        representation['product'] = product_name
        representation['group'] = group_name
        return representation
