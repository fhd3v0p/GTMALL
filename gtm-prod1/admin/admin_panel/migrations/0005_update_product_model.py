# Generated manually on 2025-08-05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_add_is_active_to_category'),
    ]

    operations = [
        # Сначала удаляем проблемные таблицы, если они существуют
        migrations.RunSQL(
            "DROP TABLE IF EXISTS product_gallery CASCADE;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS product_views CASCADE;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS product_likes CASCADE;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS product_comments CASCADE;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS sales CASCADE;",
            reverse_sql=""
        ),
        
        # Удаляем старую таблицу products
        migrations.RunSQL(
            "DROP TABLE IF EXISTS products CASCADE;",
            reverse_sql=""
        ),
        
        # Создаем новую таблицу products
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название товара')),
                ('category', models.CharField(max_length=255, verbose_name='Категория')),
                ('subcategory', models.CharField(
                    blank=True,
                    choices=[
                        ('pants', 'Штаны'),
                        ('outerwear', 'Верхняя одежда'),
                        ('shoes', 'Обувь'),
                        ('tshirt', 'Футболка'),
                        ('skirt', 'Юбка'),
                        ('dress', 'Платье'),
                        ('accessory', 'Аксессуар'),
                    ],
                    max_length=50,
                    verbose_name='Подкатегория'
                )),
                ('brand', models.CharField(blank=True, max_length=255, verbose_name='Бренд')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('summary', models.TextField(blank=True, verbose_name='Краткое описание для корзины')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена (₽)')),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Старая цена (₽)')),
                ('discount_percent', models.IntegerField(default=0, verbose_name='Скидка (%)')),
                ('size', models.CharField(max_length=50, verbose_name='Общий размер')),
                ('size_type', models.CharField(
                    choices=[
                        ('clothing', 'Одежда'),
                        ('shoes', 'Обувь'),
                        ('one_size', 'Один размер'),
                    ],
                    default='clothing',
                    max_length=20,
                    verbose_name='Тип размера'
                )),
                ('size_clothing', models.CharField(blank=True, max_length=10, verbose_name='Размер одежды (S, M, L, XL)')),
                ('size_pants', models.CharField(blank=True, max_length=10, verbose_name='Размер штанов')),
                ('size_shoes_eu', models.IntegerField(blank=True, null=True, verbose_name='EU размер обуви')),
                ('color', models.CharField(blank=True, max_length=255, verbose_name='Цвет')),
                ('master_telegram', models.CharField(blank=True, max_length=255, verbose_name='Telegram мастера')),
                ('avatar', models.TextField(blank=True, verbose_name='Главная фото товара')),
                ('gallery', models.JSONField(default=list, verbose_name='Галерея товара')),
                ('is_new', models.BooleanField(default=False, verbose_name='Новинка')),
                ('is_available', models.BooleanField(default=True, verbose_name='Доступен')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.artist', verbose_name='Мастер')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'products',
            },
        ),
    ] 