from base64 import b64encode

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import Application


class Command(BaseCommand):
    help = 'Creates an oauth2-Application that represents a client and is used for its authentication procedure'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, required=True)
        parser.add_argument('-a', '--app_name', type=str, required=True)
        parser.add_argument('-c', '--client_type', type=str, default=Application.CLIENT_PUBLIC)
        parser.add_argument('-g', '--grant_type', type=str, default=Application.GRANT_PASSWORD)

    def handle(self, *args, **options):
        username = options['username']

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('User named "{}" does not exist'.format(username))

        if not user.is_superuser:
            raise CommandError('User named "{}" is not a superuser'.format(username))

        app_name = options['app_name']
        client_type = options['client_type']
        grant_type = options['grant_type']

        try:
            app = Application.objects.get(user=user, name=app_name)
            success_message = '\nApplication named {app_name} already exists.'.format(app_name=app_name)
            self.stdout.write(self.style.SUCCESS(success_message))
            self._print_app_info(app=app)
        except Application.DoesNotExist:
            app = Application.objects.create(
                user=user, name=app_name, client_type=client_type, authorization_grant_type=grant_type)
            success_message = '\nCreated application named {app_name}'.format(app_name=app_name)
            self.stdout.write(self.style.SUCCESS(success_message))
            self._print_app_info(app=app)

    ### PRIVATE ###

    def _print_app_info(self, app: Application):
        def generate_client_token(client_id: str, client_secret: str):
            return b64encode((client_id + ':' + client_secret).encode('utf-8'))

        client_id = app.client_id
        client_secret = app.client_secret
        client_token = generate_client_token(client_id, client_secret)

        info_message = '\n'.join((
            '\n##################################',
            'Application: {}'.format(app),
            'client_type: {}'.format(app.client_type),
            'grant_type: {}'.format(app.authorization_grant_type),
            'client_id: {}'.format(client_id),
            'client_secret: {}'.format(client_secret),
            'client_token(b64): {}'.format(client_token),
            '##################################\n',
        ))

        self.stdout.write(self.style.SUCCESS(info_message))
