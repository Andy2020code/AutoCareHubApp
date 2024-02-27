# Generated by Django 5.0.2 on 2024-02-27 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intents_model_00',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=100)),
                ('patterns', models.TextField()),
                ('responses', models.TextField()),
                ('context', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Intents_model_01',
        ),
    ]