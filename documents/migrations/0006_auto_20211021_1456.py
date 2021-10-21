# Generated by Django 3.2.7 on 2021-10-21 14:56

from django.db import migrations, models
import django.db.models.deletion

def forwards_func(apps, schema_editor):
    Document = apps.get_model('documents', 'Document')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    new_ct = ContentType.objects.get_for_model(Document)
    Document.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('documents', '0005_auto_20211021_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audiodocument',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AddField(
            model_name='document',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_documents.document_set+', to='contenttypes.contenttype'),
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
