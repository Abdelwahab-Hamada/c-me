from django.db import migrations

def create_test_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Chat = apps.get_model('chat', 'Chat')
    ChatMessage = apps.get_model('chat', 'ChatMessage')

    # Créer des utilisateurs de test
    user1 = User.objects.create_user(username='user1', password='password')
    user2 = User.objects.create_user(username='user2', password='password')

    # Créer un chat entre les deux utilisateurs
    chat = Chat.create_if_not_exists(user1, user2)

    # Ajouter des messages de test
    ChatMessage.objects.create(sender=user1, chat=chat, text="Hello, how are you?")
    ChatMessage.objects.create(sender=user2, chat=chat, text="I'm fine, thank you!")

class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),  # Remplacez '0001_initial' par votre dernière migration
    ]

    operations = [
        migrations.RunPython(create_test_data),
    ]
