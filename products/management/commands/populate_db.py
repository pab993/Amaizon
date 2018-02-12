from django.core.management.base import BaseCommand
from products.models import Product, Assessment, UserProfile, ControlPanel
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
             20.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\Cuphead.jpg', '2017-09-05 00:00:00'],
            ['Binding of Isaac', 'The Binding of Isaac is an indie roguelike video game designed by Edmund McMillen and Florian Himsl, initially released in 2011 for Microsoft Windows; the game was later ported for OS X, and Linux operating systems.', 20.0, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\binding_of_isaac.jpg',
             '2014-05-20 00:00:00'],
            ['The legend of Zelda: Breath of the Wild', 'The Legend of Zelda: Breath of the Wild is an action-adventure video game developed and published by Nintendo for the Nintendo Switch and Wii U video game consoles. The game is a part of The Legend of Zelda series, and follows amnesiac protagonist Link, who awakens from a hundred-year slumber to a mysterious voice that guides him to defeat Calamity Ganon before he can destroy the kingdom of Hyrule.',
             49.99, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\zelda.jpg', '2017-03-12 00:00:00'],
            ['Watch Dogs', 'Watch Dogs (stylized as WATCH_DOGS) is an action-adventure video game developed by Ubisoft Montreal and published by Ubisoft.', 35.69, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\watchdogs.jpg', '2015-11-01 00:00:00'],
            ['BloodBorne', "Bloodborne is an action role-playing video game developed by FromSoftware and published by Sony Computer Entertainment for PlayStation 4. Officially announced at Sony's Electronic Entertainment Expo 2014 conference, the game was released worldwide in March 2015.", 39.99, 'C:\\Users\\pab99\\Documents\\TFG\\Amaizon\\media\\bloodborne.png', '2015-07-05 00:00:00']]

        amaizon_users = [['user1', 'user1', 'user1@user1.com'], ['user2', 'user2', 'user2@user2.com'], ['user3', 'user3', 'user3@user3.com'], ['user4', 'user4', 'user4@user4.com'], ['user5', 'user5', 'user5@user5.com'], ['user6', 'user6', 'user6@user6.com'], ['user7', 'user7', 'user7@user7.com'], ['user8', 'user8', 'user8@user8.com'], ['user9', 'user9', 'user9@user9.com'], ['user10', 'user10', 'user10@user10.com']]
        amaizon_superusers = [['admin123', 'admin123', 'admin123@admin123.com']]

        #El tamaño de esta tupla debe ser menor que las de users y products para que funcione la populación
        amaizon_assessment = [['I love it', '4', '2017-10-05 10:00:00'],
                              ["I recommended, it's the perfect game", '5', '2017-10-25 15:10:00'],
                              ["This is bull****, I don't like it", '1', '2017-11-01 12:30:00'],
                              ['No era lo que esperaba, pero estoy satisfecho', '3', '2017-11-01 12:30:00'],
                              ["I love this game, its artistic direction, the music and the gameplay", '4', '2017-09-23 12:33:00'],
                              ['This is awesome', '5', '2017-11-07 06:18:00'],
                              ["It's a good game indeed", '4', '2017-11-09 11:03:00'],
                              ["Meh... I've seen better things", '1', '2017-10-11 12:30:00'],
                              ['No estoy satisfecho, pero era lo que esperaba', '2', '2017-11-01 16:45:00'],
                              ["It's very good, everybody that loves games should try this one", '4', '2017-10-28 12:30:00'],
                              ["This is a very long comment, because I want to make a good review of this game. Well, actually, I've never play this game but my friends told me that it's great so... I guess it's good. Ok, I lied... I don't have any friends...", '5', '2017-11-05 19:22:00'],
                              ["Cuphead is a mater piece, a great work of art", "5", "2017-11-25 14:00:21"],
                              ["The binding of isaac is a game very hard but the effort is worth it", "4", "2016-04-10 17:43:22"],
                              ["Miyazaki is the boss of FromSoftware. I love every game of him", "5", "2016-05-11 01:32:11"],
                              ["I don't like cuphead because I don't like plataform games", "1", "2017-09-21 20:12:21"],
                              ["I love all the games of Zelda", "5", "2017-12-11 12:12:12"],
                              ["This game is very expensive", "2", "2015-12-02 08:00:12"],
                              ["This game is innapropiate. It should be for adults.", "1", "2016-03-03 11:23:22"],
                              ["Undertale is the best indi game I've ever played, 10/10", "5", "2015-08-20 10:09:10"],
                              ["Watch dogs is a magnificent game. I recommend it highly.", "4", "2016-04-01 12:55:11"],
                              ["The best RPG ever created", "5", "2014-12-28 13:13:13"],
                              ["This is a great game", "5", "2017-07-22 09:22:00"],
                              ["This game sucks. I prefer the fifa because I don't have any idea about games", "1", "2017-07-12 05:45:22"],
                              ["¿Bloodborne? More like BloodBored", "2", "2017-01-12 15:34:09"],
                              ["This game is overrated, but still it is a good game", "3", "2017-03-05 21:22:22"],
                              ["Haha, This game it's so funny! Because it's very bad >:(", "1", "2015-06-03 22:50:45"],
                              ["I'm still waiting for the remake, The hero of Time", "4", "2016-10-29 23:02:56"],
                              ["I dont like it. The reason is because the draws are not of my style", "2", "2017-06-02 04:37:03"],
                              ["For honor doesn't have dedicated server, and his community is terrible. Sorry but I have to rate this badly.", "1", "2017-02-26 09:04:45"],
                              ["The story and the music of this game is wonderful", "5", "2015-10-05 20:53:22"],
                              ["I can't wait to play it", "5", "2017-01-21 21:21:21"],
                              ["Meh, I don't want to even play it", "2", "2015-04-05 22:22:23"],
                              ["Undertale, YEAH!", "4", "2015-06-05 23:22:23"],
                              ["Zelda! Zelda! Link! Link!", "4", "2017-06-05 21:23:12"],
                              ["It is like DS but darker, and the combat it is faster too", "5", "2016-11-11 17:23:15"],
                              ["Dank Sauce for the win!", "5", "2018-01-04 12:12:12"],
                              ["The multiplayer of this game make it too easy from my point of view", "4", "2018-01-09 11:12:14"],
                              ["It is ok I guess", "3", "2017-12-26 09:09:12"],
                              ["Stay determinated", "3", "2017-11-20 20:14:02"],
                              ["I recommend this game, my friends recommend it and my grandmother recommend it", "5", "2014-12-11 13:23:02"],
                              ["I don't like anything from NINTENDO", "1", "2016-09-08 01:01:34"],
                              ["This game is totally toxic", "2", "2017-06-11 11:11:11"],
                              ["One of the best things about The Binding of Isaac: Rebirth is that every time I play, Isaac ends up looking and behaving radically differently", "4", "2016-12-12 13:14:15"],
                              ["Stop making bad game ubisoft. First Warning", "1", "2015-07-28 11:34:23"],
                              ["Bloodborne is only for PS4 sadly, but anyway is a good game", "4", "2016-12-10 12:34:56"],
                              ["Praise the sun!", "5", "2017-08-11 16:19:45"],
                              ["Too expensive, and the game doesnt have dedicated servers", "1", "2017-03-03 14:34:46"],
                              ["Rogue dungeons are games with something special", "3", "2017-05-11 19:19:35"],
                              ["Nothing innovative", "2", "2015-09-11 23:13:34"],
                              ["Muzska, I'm still waiting for 'Poniendo a parir Bloodborne'", "5", "2018-02-01 18:45:12"]]

        for i in range(len(amaizon_products)):
            f = open(amaizon_products[i][3], 'rb')
            p = Product(name=amaizon_products[i][0], description=amaizon_products[i][1], price=amaizon_products[i][2],
                        picture=File(f), pub_date=amaizon_products[i][4])
            p.save()

        for j in range(len(amaizon_users)):
            u = User.objects.create_user(username=amaizon_users[j][0], email=amaizon_users[j][2], password=amaizon_users[j][1])
            u.save()
            user_profile = UserProfile(user=u)
            user_profile.save()

        p = Product.objects.all()
        u = User.objects.all()

        a0 = Assessment(comment=amaizon_assessment[0][0], score=amaizon_assessment[0][1], post_date=amaizon_assessment[0][2], product=p[0], user=u[0])
        a0.save()
        a1 = Assessment(comment=amaizon_assessment[1][0], score=amaizon_assessment[1][1], post_date=amaizon_assessment[1][2], product=p[1], user=u[0])
        a1.save()
        a2 = Assessment(comment=amaizon_assessment[2][0], score=amaizon_assessment[2][1], post_date=amaizon_assessment[2][2], product=p[0], user=u[1])
        a2.save()
        a3 = Assessment(comment=amaizon_assessment[3][0], score=amaizon_assessment[3][1], post_date=amaizon_assessment[3][2], product=p[3], user=u[2])
        a3.save()
        a4 = Assessment(comment=amaizon_assessment[4][0], score=amaizon_assessment[4][1], post_date=amaizon_assessment[4][2], product=p[1], user=u[3])
        a4.save()
        a5 = Assessment(comment=amaizon_assessment[5][0], score=amaizon_assessment[5][1], post_date=amaizon_assessment[5][2], product=p[3], user=u[3])
        a5.save()
        a6 = Assessment(comment=amaizon_assessment[6][0], score=amaizon_assessment[6][1], post_date=amaizon_assessment[6][2], product=p[4], user=u[4])
        a6.save()
        a7 = Assessment(comment=amaizon_assessment[7][0], score=amaizon_assessment[7][1], post_date=amaizon_assessment[7][2], product=p[6], user=u[6])
        a7.save()
        a8 = Assessment(comment=amaizon_assessment[8][0], score=amaizon_assessment[8][1], post_date=amaizon_assessment[8][2], product=p[7], user=u[1])
        a8.save()
        a9 = Assessment(comment=amaizon_assessment[9][0], score=amaizon_assessment[9][1], post_date=amaizon_assessment[9][2], product=p[1], user=u[1])
        a9.save()
        a10 = Assessment(comment=amaizon_assessment[10][0], score=amaizon_assessment[10][1], post_date=amaizon_assessment[10][2], product=p[5], user=u[9])
        a10.save()
        #Nuevas reviews
        a11 = Assessment(comment=amaizon_assessment[11][0], score=amaizon_assessment[11][1], post_date=amaizon_assessment[11][2], product=p[3], user=u[4])
        a11.save()
        a12 = Assessment(comment=amaizon_assessment[12][0], score=amaizon_assessment[12][1], post_date=amaizon_assessment[12][2], product=p[4], user=u[2])
        a12.save()
        a13 = Assessment(comment=amaizon_assessment[13][0], score=amaizon_assessment[13][1], post_date=amaizon_assessment[13][2], product=p[7], user=u[2])
        a13.save()
        a14 = Assessment(comment=amaizon_assessment[14][0], score=amaizon_assessment[14][1], post_date=amaizon_assessment[14][2], product=p[3], user=u[0])
        a14.save()
        a15 = Assessment(comment=amaizon_assessment[15][0], score=amaizon_assessment[15][1],
                         post_date=amaizon_assessment[15][2], product=p[5], user=u[0])
        a15.save()
        a16 = Assessment(comment=amaizon_assessment[16][0], score=amaizon_assessment[16][1],
                         post_date=amaizon_assessment[16][2], product=p[6], user=u[0])
        a16.save()
        a17 = Assessment(comment=amaizon_assessment[17][0], score=amaizon_assessment[17][1],
                         post_date=amaizon_assessment[17][2], product=p[4], user=u[1])
        a17.save()
        a18 = Assessment(comment=amaizon_assessment[18][0], score=amaizon_assessment[18][1],
                         post_date=amaizon_assessment[18][2], product=p[2], user=u[1])
        a18.save()
        a19 = Assessment(comment=amaizon_assessment[19][0], score=amaizon_assessment[19][1],
                         post_date=amaizon_assessment[19][2], product=p[6], user=u[2])
        a19.save()
        a20 = Assessment(comment=amaizon_assessment[20][0], score=amaizon_assessment[20][1],
                         post_date=amaizon_assessment[20][2], product=p[0], user=u[2])
        a20.save()
        a21 = Assessment(comment=amaizon_assessment[21][0], score=amaizon_assessment[21][1],
                         post_date=amaizon_assessment[21][2], product=p[5], user=u[3])
        a21.save()
        a22 = Assessment(comment=amaizon_assessment[22][0], score=amaizon_assessment[22][1],
                         post_date=amaizon_assessment[22][2], product=p[2], user=u[3])
        a22.save()
        a23 = Assessment(comment=amaizon_assessment[23][0], score=amaizon_assessment[23][1],
                         post_date=amaizon_assessment[23][2], product=p[7], user=u[3])
        a23.save()
        a24 = Assessment(comment=amaizon_assessment[24][0], score=amaizon_assessment[24][1],
                         post_date=amaizon_assessment[24][2], product=p[0], user=u[4])
        a24.save()
        a25 = Assessment(comment=amaizon_assessment[25][0], score=amaizon_assessment[25][1],
                         post_date=amaizon_assessment[25][2], product=p[6], user=u[4])
        a25.save()
        a26 = Assessment(comment=amaizon_assessment[26][0], score=amaizon_assessment[26][1],
                         post_date=amaizon_assessment[26][2], product=p[5], user=u[4])
        a26.save()
        a27 = Assessment(comment=amaizon_assessment[27][0], score=amaizon_assessment[27][1],
                         post_date=amaizon_assessment[27][2], product=p[3], user=u[5])
        a27.save()
        a28 = Assessment(comment=amaizon_assessment[28][0], score=amaizon_assessment[28][1],
                         post_date=amaizon_assessment[28][2], product=p[1], user=u[5])
        a28.save()
        a29 = Assessment(comment=amaizon_assessment[29][0], score=amaizon_assessment[29][1],
                         post_date=amaizon_assessment[29][2], product=p[2], user=u[5])
        a29.save()
        a30 = Assessment(comment=amaizon_assessment[30][0], score=amaizon_assessment[30][1],
                         post_date=amaizon_assessment[30][2], product=p[5], user=u[5])
        a30.save()
        a31 = Assessment(comment=amaizon_assessment[31][0], score=amaizon_assessment[31][1],
                         post_date=amaizon_assessment[31][2], product=p[6], user=u[5])
        a31.save()
        a32 = Assessment(comment=amaizon_assessment[32][0], score=amaizon_assessment[32][1],
                         post_date=amaizon_assessment[32][2], product=p[2], user=u[6])
        a32.save()
        a33 = Assessment(comment=amaizon_assessment[33][0], score=amaizon_assessment[33][1],
                         post_date=amaizon_assessment[33][2], product=p[5], user=u[6])
        a33.save()
        a34 = Assessment(comment=amaizon_assessment[34][0], score=amaizon_assessment[34][1],
                         post_date=amaizon_assessment[34][2], product=p[7], user=u[6])
        a34.save()
        a35 = Assessment(comment=amaizon_assessment[35][0], score=amaizon_assessment[35][1],
                         post_date=amaizon_assessment[35][2], product=p[0], user=u[6])
        a35.save()
        a36 = Assessment(comment=amaizon_assessment[36][0], score=amaizon_assessment[36][1],
                         post_date=amaizon_assessment[36][2], product=p[3], user=u[7])
        a36.save()
        a37 = Assessment(comment=amaizon_assessment[37][0], score=amaizon_assessment[37][1],
                         post_date=amaizon_assessment[37][2], product=p[1], user=u[7])
        a37.save()
        a38 = Assessment(comment=amaizon_assessment[38][0], score=amaizon_assessment[38][1],
                         post_date=amaizon_assessment[38][2], product=p[2], user=u[7])
        a38.save()
        a39 = Assessment(comment=amaizon_assessment[39][0], score=amaizon_assessment[39][1],
                         post_date=amaizon_assessment[39][2], product=p[4], user=u[7])
        a39.save()
        a40 = Assessment(comment=amaizon_assessment[40][0], score=amaizon_assessment[40][1],
                         post_date=amaizon_assessment[40][2], product=p[5], user=u[7])
        a40.save()
        a41 = Assessment(comment=amaizon_assessment[41][0], score=amaizon_assessment[41][1],
                         post_date=amaizon_assessment[41][2], product=p[1], user=u[8])
        a41.save()
        a42 = Assessment(comment=amaizon_assessment[42][0], score=amaizon_assessment[42][1],
                         post_date=amaizon_assessment[42][2], product=p[4], user=u[8])
        a42.save()
        a43 = Assessment(comment=amaizon_assessment[43][0], score=amaizon_assessment[43][1],
                         post_date=amaizon_assessment[43][2], product=p[6], user=u[8])
        a43.save()
        a44 = Assessment(comment=amaizon_assessment[44][0], score=amaizon_assessment[44][1],
                         post_date=amaizon_assessment[44][2], product=p[7], user=u[8])
        a44.save()
        a45 = Assessment(comment=amaizon_assessment[45][0], score=amaizon_assessment[45][1],
                         post_date=amaizon_assessment[45][2], product=p[0], user=u[8])
        a45.save()
        a46 = Assessment(comment=amaizon_assessment[46][0], score=amaizon_assessment[46][1],
                         post_date=amaizon_assessment[46][2], product=p[1], user=u[9])
        a46.save()
        a47 = Assessment(comment=amaizon_assessment[47][0], score=amaizon_assessment[47][1],
                         post_date=amaizon_assessment[47][2], product=p[4], user=u[9])
        a47.save()
        a48 = Assessment(comment=amaizon_assessment[48][0], score=amaizon_assessment[48][1],
                         post_date=amaizon_assessment[48][2], product=p[6], user=u[9])
        a48.save()
        a49 = Assessment(comment=amaizon_assessment[49][0], score=amaizon_assessment[49][1],
                         post_date=amaizon_assessment[49][2], product=p[7], user=u[9])
        a49.save()


        for z in range(len(amaizon_superusers)):
            u = User.objects.create_user(username=amaizon_superusers[z][0], email=amaizon_superusers[z][2], password=amaizon_superusers[z][1])
            u.is_staff = True
            u.is_admin = True
            u.is_superuser = True
            u.save()
            user_profile = UserProfile(user=u)
            user_profile.save()

        cp = ControlPanel(threshold=0.00)
        cp.save()

    def handle(self, *args, **options):
        self._create_products()
