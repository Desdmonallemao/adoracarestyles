import os
import django
from django.core.management import call_command

# Configurer l’environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adora.settings")
django.setup()

# Charger les données depuis le fichier JSON
try:
    call_command("loaddata", "db.json")
    print("✅ Données importées avec succès dans PostgreSQL.")
except Exception as e:
    print("❌ Erreur pendant l'import :", e)
