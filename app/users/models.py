from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Max
from datetime import date
from django.db import models


class UserProfile(models.Model):
    GENDER_CHOICES = {
        0: 'не указан',
        1: 'мужской',
        2: 'женский',
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='profile')
    gender = models.SmallIntegerField('Пол', choices=GENDER_CHOICES, default=0)
    family = models.CharField('Фамилия', max_length=30)
    name = models.CharField('Имя', max_length=30)
    surname = models.CharField('Отчество', max_length=30, blank=True)
    description = models.TextField('Описание', blank=True)
    tester = models.BooleanField('Тестировщик', default=False)
    date = models.DateField('Дата приема', default=date.today)

    @property
    def diff_date(self):
        return (date.today() - self.date).days

    class Meta:
        ordering = ['-date',]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.family} {self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Desks.objects.filter(user_id=self.id).exists():
            Desks.objects.create(user_id=self.id)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

class SkillList(models.Model):
    skill = models.CharField('Название', unique=True)

    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = 'Список навыков'

    def __str__(self):
        return f'{self.skill}'

class Skills(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='skills')
    skill = models.ForeignKey(SkillList, on_delete=models.CASCADE, verbose_name='Навык', related_name='users')
    level = models.SmallIntegerField('Уровень освоения', choices=[(a, a) for a in range(1, 11)])

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return f'{self.skill}: {self.level}'

class Desks(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='desk')
    number = models.PositiveSmallIntegerField('Номер стола', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f'{self.number}: {self.user}'

    def clean(self):
        if self.number:
            this_desk = Desks.objects.filter(number=self.number).exclude(user=self.user).first()
            if this_desk and this_desk.number == self.number:
                raise ValidationError('Это место уже занято.')
            current_user = self.user.tester
            neigh1 = Desks.objects.filter(number=self.number - 1).first()
            neigh2 = Desks.objects.filter(number=self.number + 1).first()
            if neigh1:
                if neigh1.user.tester != current_user:
                    raise ValidationError('Тестировщики и разработчики не должны сидеть за соседними столами.')
            if neigh2:
                if neigh2.user.tester != current_user:
                    raise ValidationError('Тестировщики и разработчики не должны сидеть за соседними столами.')

class Gallery(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='gallery')
    image = models.ImageField('Изображение')
    position = models.PositiveSmallIntegerField('Позиция', default=0)

    class Meta:
        ordering = ['position',]
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея'

    def save(self, *args, **kwargs):
        if not self.position:
            last_position = Gallery.objects.filter(user=self.user).aggregate(Max('position'))['position__max']
            self.position = 1 if last_position is None else last_position + 1
        super().save(*args, **kwargs)
