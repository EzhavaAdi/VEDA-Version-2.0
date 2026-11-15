from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('inventory', '0002_shop')]
    operations = [
        migrations.AddField(
            model_name='shopproduct',
            name='image_path',
            field=models.CharField(blank=True, max_length=200, help_text='Filename in /shop/ folder'),
        ),
    ]
