from django.core.management.base import BaseCommand
from cardapp.models import (
    Card,
    Prices,
    Rulings,
    CardImage
)

class Command(BaseCommand):
    help = "Deletes all records from the database"

    def handle(self, *args, **options):
        batch_size = 100  # Set your batch size here

        model_names_input = input("Enter the model names separated by commas (or 'all_models' for all models): ")
        if model_names_input.lower() == 'all_models':
            model_names = ['Card','Prices','Rulings','CardImage']
        else:
            model_names = [name.strip() for name in model_names_input.split(',')]

        for model_name in model_names:
            try:
                model = globals()[model_name]
            except KeyError:
                self.stdout.write(self.style.ERROR(f"Model '{model_name}' not found"))
                continue

            while True:
                records = model.objects.all()[:batch_size]
                if not records:
                    break
                model.objects.filter(pk__in=records.values_list("pk", flat=True)).delete()
                self.stdout.write(self.style.SUCCESS(f"{batch_size} records deleted for model '{model_name}'"))