# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0006_add_https_image_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveaway',
            name='app_button_enabled',
            field=models.BooleanField(default=True, verbose_name="Кнопка 'Перейти в приложение' активна"),
        ),
    ] 