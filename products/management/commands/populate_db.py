from django.core.management.base import BaseCommand
from products.models import Product
from django.contrib.auth.models import User
from django.core.files import File


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_products(self):
        amaizon_products = [
            ['Dark Souls', 'Dark Souls is an action role-playing video game developed by FromSoftware', 15.0,
             'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\Dark_Souls_Portada.jpg', '2011-12-18 00:00:00'],
            ['For honor', 'For Honor is a hack and slash fighting game developed and published by Ubisoft for Microsoft Windows, PlayStation 4, and Xbox One',
             45.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\ForHonor.jpg', '2016-10-05 00:00:00'],
            ['Undertale', 'Undertale is a role-playing video game created by American indie developer and composer Toby Fox. In the game, players control a human child who has fallen into the Underground, a large, secluded region underneath the surface of the Earth, separated by a magic barrier',
             15.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\Undertale.png', '2015-06-25 00:00:00'],
            ['Cuphead', 'Cuphead is a classic run and gun action game heavily focused on boss battles. Inspired by cartoons of the 1930s, the visuals and audio are painstakingly created with the same techniques of the era, i.e. traditional hand drawn cel animation, watercolor backgrounds, and original jazz recordings',
             20.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\Cuphead.jpg', '2017-10-05 00:00:00']]

        amaizon_users = [['user1', 'user1'], ['user2', 'user2'], ['user3', 'user3'], ['user4', 'user4'], ['user5', 'user5'], ['user6', 'user6'], ['user7', 'user7'], ['user8', 'user8'], ['user9', 'user9'], ['user10', 'user10']]

        for i in range(len(amaizon_products)):
            f = open(amaizon_products[i][3], 'rb')
            p = Product(name=amaizon_products[i][0], description=amaizon_products[i][1], price=amaizon_products[i][2],
                        picture=File(f), pub_date=amaizon_products[i][4])
            p.save()

        for j in range(len(amaizon_users)):
            u = User(username=amaizon_users[j][0], password=amaizon_users[j][1])
            u.save()

    def handle(self, *args, **options):
        self._create_products()
