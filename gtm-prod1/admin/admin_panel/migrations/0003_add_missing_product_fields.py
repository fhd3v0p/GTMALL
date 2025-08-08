# Generated manually on 2025-08-05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_add_gallery_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='summary',
            field=models.TextField(blank=True, verbose_name='Краткое описание для корзины'),
        ),
        migrations.AddField(
            model_name='product',
            name='size_type',
            field=models.CharField(
                choices=[('clothing', 'Одежда'), ('shoes', 'Обувь'), ('one_size', 'Один размер')],
                default='clothing',
                max_length=20,
                verbose_name='Тип размера'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='size_clothing',
            field=models.CharField(blank=True, max_length=10, verbose_name='Размер одежды (S, M, L, XL)'),
        ),
        migrations.AddField(
            model_name='product',
            name='size_pants',
            field=models.CharField(blank=True, max_length=10, verbose_name='Размер штанов'),
        ),
        migrations.AddField(
            model_name='product',
            name='size_shoes_eu',
            field=models.IntegerField(blank=True, null=True, verbose_name='EU размер обуви'),
        ),
    ] 