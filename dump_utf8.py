import os
import django
from django.core.management import call_command

# Spécifie le module de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adora.settings')

# Initialise Django
django.setup()

# Ouvre un fichier avec encodage UTF-8 explicite
with open('db.json', 'w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        use_natural_primary_keys=True,
        use_natural_foreign_keys=True,
        indent=2,
        stdout=f
    )
