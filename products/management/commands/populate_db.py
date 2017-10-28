from django.core.management.base import BaseCommand
from products.models import Product, Assessment
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
             20.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\Cuphead.jpg', '2017-10-05 00:00:00'],
            ['Binding of Isaac', 'The Binding of Isaac is an indie roguelike video game designed by Edmund McMillen and Florian Himsl, initially released in 2011 for Microsoft Windows; the game was later ported for OS X, and Linux operating systems.', 20.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\binding_of_isaac.jpg',
             '2014-05-20 00:00:00'],
            ['The legend of Zelda: Breath of the Wild', 'The Legend of Zelda: Breath of the Wild is an action-adventure video game developed and published by Nintendo for the Nintendo Switch and Wii U video game consoles. The game is a part of The Legend of Zelda series, and follows amnesiac protagonist Link, who awakens from a hundred-year slumber to a mysterious voice that guides him to defeat Calamity Ganon before he can destroy the kingdom of Hyrule.',
             49.99, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\zelda.jpg', '2017-03-12 00:00:00'],
            ['Watch Dogs', 'Watch Dogs (stylized as WATCH_DOGS) is an action-adventure video game developed by Ubisoft Montreal and published by Ubisoft.', 35.69, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\watchdogs.jpg', '2015-11-01 00:00:00'],
            ['BloodBorne', "Bloodborne is an action role-playing video game developed by FromSoftware and published by Sony Computer Entertainment for PlayStation 4. Officially announced at Sony's Electronic Entertainment Expo 2014 conference, the game was released worldwide in March 2015.", 39.99, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\bloodborne.png', '2015-07-05 00:00:00']]

        amaizon_users = [['user1', 'user1', 'user1@user1.com'], ['user2', 'user2', 'user2@user2.com'], ['user3', 'user3', 'user3@user3.com'], ['user4', 'user4', 'user4@user4.com'], ['user5', 'user5', 'user5@user5.com'], ['user6', 'user6', 'user6@user6.com'], ['user7', 'user7', 'user7@user7.com'], ['user8', 'user8', 'user8@user8.com'], ['user9', 'user9', 'user9@user9.com'], ['user10', 'user10', 'user10@user10.com']]

        #El tamaño de esta tupla debe ser menor que las de users y products para que funcione la populación
        amaizon_assessment = [['I love it', '4'], ["I recommended, it's the perfect game", '5'], ["This is bull****, I don't like it", '0'], ['No era lo que esperaba, pero estoy satidfecho', '3'], ["I love this game, its artistic direction, the music and the gameplay", '4']]

        amaizon_assessment2 = [['This is awesome', '5'], ["It's a good game indeed", '4'],
                              ["Meh... I've seen better things", '1'],
                              ['No estoy satisfecho, pero era lo que esperaba', '2'],
                              ["It's very good, everybody that loves games should try this one", '4'],]


        for i in range(len(amaizon_products)):
            f = open(amaizon_products[i][3], 'rb')
            p = Product(name=amaizon_products[i][0], description=amaizon_products[i][1], price=amaizon_products[i][2],
                        picture=File(f), pub_date=amaizon_products[i][4])
            p.save()

        for j in range(len(amaizon_users)):
            #u = User(username=amaizon_users[j][0], password=amaizon_users[j][1])
            u = User.objects.create_user(username=amaizon_users[j][0], email=amaizon_users[j][2], password=amaizon_users[j][1])
            u.save()

        p = Product.objects.all()
        u = User.objects.all()

        for e in range(len(amaizon_assessment)):
            a = Assessment(comment=amaizon_assessment[e][0], score=amaizon_assessment[e][1], product=p[e], user=u[e])
            a.save()

        for x in range(len(amaizon_assessment2)):
            a = Assessment(comment=amaizon_assessment[x][0], score=amaizon_assessment[x][1], product=p[x+1], user=u[x+1])
            a.save()


    def handle(self, *args, **options):
        self._create_products()
