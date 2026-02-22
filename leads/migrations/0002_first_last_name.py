# Generated manually for first_name/last_name migration

from django.db import migrations, models


def migrate_prospect_name(apps, schema_editor):
    Lead = apps.get_model('leads', 'Lead')
    for lead in Lead.objects.all():
        parts = (lead.prospect_name or '').strip().split(None, 1)
        lead.first_name = parts[0][:100] if parts else ''
        lead.last_name = (parts[1][:100] if len(parts) > 1 else '')
        lead.save()


def reverse_migrate(apps, schema_editor):
    Lead = apps.get_model('leads', 'Lead')
    for lead in Lead.objects.all():
        lead.prospect_name = f"{lead.first_name} {lead.last_name}".strip()
        lead.save()


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.RunPython(migrate_prospect_name, reverse_migrate),
        migrations.RemoveField(
            model_name='lead',
            name='prospect_name',
        ),
        migrations.AlterField(
            model_name='lead',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
    ]
