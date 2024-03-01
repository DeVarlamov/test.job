from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    student_counter = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(30)
        ],
        error_messages={
            'min_value': 'Указано слишком маленькое значение',
            'max_value': 'Указано слишком большое значение'
        }
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_link = models.URLField()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f'{self.name} группа продукта {self.product}'


class Purchase(models.Model):
    buyer = models.ForeignKey(User,
                              related_name='buyers',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.buyer} выбрал {self.product}'
