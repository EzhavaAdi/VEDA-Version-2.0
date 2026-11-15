from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('icon', models.CharField(blank=True, help_text='Emoji icon', max_length=10)),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'db_table': 'shop_category', 'ordering': ['sort_order', 'name']},
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('part_number', models.CharField(blank=True, max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('unit', models.CharField(default='piece', max_length=30)),
                ('image_emoji', models.CharField(default='🔧', help_text='Emoji used as placeholder image', max_length=10)),
                ('compatible_with', models.CharField(blank=True, help_text='Comma-separated component codes', max_length=300)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.shopcategory')),
            ],
            options={'db_table': 'shop_product', 'ordering': ['category', 'name']},
        ),
        migrations.CreateModel(
            name='ShopCartEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_id', models.CharField(blank=True, max_length=64)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_events', to='inventory.shopproduct')),
            ],
            options={'db_table': 'shop_cart_event', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='APSPredictionLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_id', models.CharField(blank=True, max_length=64)),
                ('filename', models.CharField(blank=True, max_length=200)),
                ('predicted_class', models.CharField(max_length=10)),
                ('probability_pos', models.FloatField(blank=True, null=True)),
                ('feature_coverage', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={'db_table': 'aps_prediction_log', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='MechanicPredictionLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_id', models.CharField(blank=True, max_length=64)),
                ('predicted_component', models.CharField(max_length=50)),
                ('confidence', models.FloatField(default=0)),
                ('input_values', models.JSONField(default=dict)),
                ('component_health', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={'db_table': 'mechanic_prediction_log', 'ordering': ['-created_at']},
        ),
    ]
