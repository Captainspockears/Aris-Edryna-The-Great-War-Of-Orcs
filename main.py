import pygame
from time import sleep

#pygame initialisation and display information

pygame.init()

monitorinfo = pygame.display.Info()
monitorwidth = monitorinfo.current_w
monitorheight = monitorinfo.current_h

widthcompratio = monitorwidth/1980
heightcompratio = monitorheight/1080

scalingfactorx = 0.35
scalingfactory = 0.35

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("RPG")

#variables
startingx = 0
startingy = 750
clock = pygame.time.Clock()

weaponx1 = 0
weaponx2 = 0
bodyx1 = 0
bodyx2 = 0
hitind = False

heal = False
healcount = 0

class Option:
    hovered = False

    def __init__(self, text, pos, color=(100, 100, 100)):
        self.text = text
        self.pos = pos
        self.color = color
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        win.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return self.color

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

#Player class
class Player(object):
    def __init__(self, x, y, width, height, weapon, body):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.isJump = False
        self.left = False
        self.right = False
        self.attack = False
        self.swordanime = False
        self.orientation = True  # True - right, False - left
        self.walkCount = 0
        self.jumpCount = 10
        self.jumpanime = 0
        self.idlecount = 0
        self.weapon = weapon
        self.body = body
        self.attackstatus = False
        self.health = 70
        self.dead = False
        #image lists
        self.walkright = []
        self.walkleft = []
        self.jumpright = []
        self.jumpleft = []
        self.idle = []
        self.attackright = []
        self.attackleft = []
        self.healthbar = []

    def damage(self, enemyweapon, weaponstatus):
        istouch = False
        istouch = Hitbox.istouching(self.body, enemyweapon)

        if istouch and weaponstatus:
            self.health = self.health - 10

        if self.health <= 0:
            self.dead = True

    def draw(self, win):
        if self.walkCount + 1 >= 15:
            self.walkCount = 0

        if self.idlecount + 1 >= 15:
            self.idlecount = 0

        if self.attack:
            if self.orientation:
                win.blit(self.attackright[self.swordanime // 2], (self.x, self.y))
            else:
                win.blit(self.attackleft[self.swordanime // 2], (self.x, self.y))
        elif self.isJump:
            if self.orientation:
                win.blit(self.jumpright[self.jumpanime // 2], (self.x, self.y))
            else:
                win.blit(self.jumpleft[self.jumpanime // 2], (self.x, self.y))
        elif self.left:
            win.blit(self.walkleft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(self.walkright[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.idle[self.idlecount // 3], (self.x, self.y))
        win.blit(self.healthbar[(self.health // 10) - 1], (int(monitorwidth*0.4), 25))
        #self.weapon.drawhitbox(win)
        #self.body.drawhitbox(win)


#Enemy class
class Enemy(object):
    def __init__(self, x, y, width, height, weapon, body):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.isJump = False
        self.left = False
        self.right = False
        self.attack = False
        self.swordanime = False
        self.orientation = True  # True - right, False - left
        self.walkCount = 0
        self.jumpCount = 10
        self.jumpanime = 0
        self.idlecount = 0
        self.attackcount = 0
        self.weapon = weapon
        self.body = body
        self.pause = True
        self.health = 70
        self.dead = False
        self.attackstatus = False
        #image lists
        self.walkright = []
        self.walkleft = []
        self.jumpright = []
        self.jumpleft = []
        self.idle = []
        self.attackright = []
        self.attackleft = []
        self.healthbar = []

    def damage(self, playerweapon, weaponstatus):
        istouch = False
        istouch = Hitbox.istouching(self.body, playerweapon)

        if istouch and weaponstatus:
            self.health = self.health - 10

        if self.health <= 0:
            self.dead = True


    def draw(self, win):
        if self.walkCount + 1 >= 21:
            self.walkCount = 0

        if self.idlecount + 1 >= 15:
            self.idlecount = 0

        if self.attackcount + 1 >= 21:
            self.attackcount = 0

        if self.attack:
            if self.orientation:
                win.blit(self.attackright[self.attackcount // 3], (self.x, self.y))
                self.attackcount += 1
            else:
                win.blit(self.attackleft[self.attackcount // 3], (self.x, self.y))
                self.attackcount += 1
        elif self.left:
            win.blit(self.walkleft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(self.walkright[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.idle[self.idlecount // 3], (self.x, self.y))
            self.idlecount += 1
        win.blit(self.healthbar[(self.health//10)-1], (self.x + 50 * widthcompratio, self.y - 50 * heightcompratio))
        #self.weapon.drawhitbox(win)
        #self.body.drawhitbox(win)

    def move(self, startposx, endposx):
        oldorient = self.orientation
        self.attackstatus = False
        if not (oldorient == self.orientation):
            oldorient = self.orientation
            self.pause = True
        if startposx == endposx:
            self.right = False
            self.left = False
            self.attack = False
            self.attackstatus = False
            self.isJump = False
            return True
        if startposx>endposx:
            self.orientation = False
            if startposx - (180 * widthcompratio) < endposx:
                if self.pause:
                    self.pause = False
                    return False
                self.weapon.x = int(self.x - 0 * widthcompratio)
                self.body.x = int(self.x + 100 * widthcompratio)
                self.attack = True
                self.attackstatus = True
                self.left = False
                self.right = False
                self.isJump = False
            else:
                self.x -= self.vel
                self.weapon.x = int(self.x - 0 * widthcompratio)
                self.body.x = int(self.x + 100 * widthcompratio)
                self.left = True
                self.right = False
                self.attack = False
                self.attackstatus = False
            return False
        else:
            self.orientation = True
            if startposx + (320 * widthcompratio) > endposx:
                if self.pause:
                    self.pause = False
                    return False
                self.weapon.x = int(self.x + 160 * widthcompratio)
                self.body.x = int(self.x + 10 * widthcompratio)
                self.attack = True
                self.attackstatus = True
                self.left = False
                self.right = False
                self.isJump = False
            else:
                self.x += self.vel
                self.weapon.x = int(self.x + 160 * widthcompratio)
                self.body.x = int(self.x + 10 * widthcompratio)
                self.left = False
                self.right = True
                self.attack = False
                self.attackstatus = False
            return False
        self.right = False
        self.left = False
        self.attack = False
        self.isJump = False
        self.attackstatus = False
        return False

#Hitbox class
class Hitbox:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def drawhitbox(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 2)

    def istouching(self, hitbox):
        global weaponx1, weaponx2, bodyx1, bodyx2, hitind
        #print("Weapon: x1 = {}, x2 = {}".format(hitbox.x, hitbox.x+hitbox.width))
        #print("Body: x1 = {}, x2 = {}".format(self.x, self.x+self.width))
        weaponx1 = int(hitbox.x)
        weaponx2 = int(hitbox.x+hitbox.width)
        bodyx1 = int(self.x)
        bodyx2 = int(self.x+self.width)
        hitind = False
        if (weaponx2>=bodyx1) and ((weaponx1)<=(bodyx2)):
            #print("touch")
            hitind = True
            return True
        return False

#Weapon class
class Weapon(Hitbox):
    def __init__(self, name, x, y, width, height):
        self.color = (255, 0, 0)
        self.name = name
        Hitbox.__init__(self, x, y, width, height, self.color)


def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'Comic Sans MS'):
    try:

        text = str(text)
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e

#redraw function
def redrawGameWindow():
    win.blit(bg, (0, 0))
    #print("attack = {}, walk = {}, idle = {} => attack = {}, walk = {}, idle = {}".format(orc.attackcount, orc.walkCount,orc.idlecount,(orc.attackcount // 2),(orc.walkCount // 3),(orc.idlecount // 3)))
    #print("Health = {}".format(orc.health))
    mainplayer.draw(win)
    orc.draw(win)
    #text_to_screen(win, "Health: {}".format(mainplayer.health), 10, 10)
    pygame.display.update()


print("monitor.width = {}, monitor.height = {}".format(monitorwidth, monitorheight))

#mainplayer initialisation
body = Hitbox(int(startingx + 10 * widthcompratio), int(startingy + 0 * heightcompratio), int(490 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio), (0, 0, 255))
weapon = Weapon('sword', int(startingx + 160 * widthcompratio), int(startingy + 60 * heightcompratio), int(250 * scalingfactorx * widthcompratio), int(500 * scalingfactory * heightcompratio))
mainplayer = Player(int(startingx * widthcompratio), int(startingy * heightcompratio), int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio), weapon, body)

#mainplayer image lists
mainplayer.walkright = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkright/2_WALK_000.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkright/2_WALK_001.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkright/2_WALK_002.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkright/2_WALK_003.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkright/2_WALK_004.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.walkleft = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkleft/2_WALK_000.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkleft/2_WALK_001.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkleft/2_WALK_002.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkleft/2_WALK_003.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Walkleft/2_WALK_004.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.jumpright = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpright/4_JUMP_000.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpright/4_JUMP_001.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpright/4_JUMP_002.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpright/4_JUMP_003.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpright/4_JUMP_004.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpright/4_JUMP_005.png'),
                                    (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.jumpleft = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpleft/4_JUMP_000.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpleft/4_JUMP_001.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpleft/4_JUMP_002.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpleft/4_JUMP_003.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpleft/4_JUMP_004.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Warrior/Jumpleft/4_JUMP_005.png'),
                                   (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.idle = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Idle/1_IDLE_000.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Idle/1_IDLE_001.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Idle/1_IDLE_002.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Idle/1_IDLE_003.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Idle/1_IDLE_004.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.attackright = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackright/5_ATTACK_000.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackright/5_ATTACK_001.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackright/5_ATTACK_002.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackright/5_ATTACK_003.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackright/5_ATTACK_004.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.attackleft = [pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackleft/5_ATTACK_000.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackleft/5_ATTACK_001.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackleft/5_ATTACK_002.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackleft/5_ATTACK_003.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Warrior/Attackleft/5_ATTACK_004.png'),
                               (int(705 * scalingfactorx * widthcompratio), int(800 * scalingfactory * heightcompratio)))]
mainplayer.healthbar = [pygame.transform.scale(pygame.image.load('Recources/Healthbar/1.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/2.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/3.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/4.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/5.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/6.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/7.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio)))]

startingx = 1500
startingy = 780
scalingfactorx = 0.2
scalingfactory = 0.2

#orc initialisation
body = Hitbox(int(startingx - 40 * widthcompratio), int(startingy), int(1140 * scalingfactorx * widthcompratio), int(1230 * scalingfactory * heightcompratio), (0, 0, 255))
weapon = Weapon('sword', int(startingx + 150 * widthcompratio), int(startingy + 100 * widthcompratio), int(840 * scalingfactorx * widthcompratio), int(600 * scalingfactory * heightcompratio))
orc = Enemy(int(startingx * widthcompratio), int(startingy * heightcompratio), int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio), weapon, body)
orc.vel = 5

#orc image lists
orc.walkleft = [pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_000.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_001.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_002.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_003.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_004.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_005.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
             pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkleft/WALK_006.png'),
                                    (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio)))]
orc.walkright = [pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_000.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_001.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_002.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_003.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_004.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_005.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
            pygame.transform.scale(pygame.image.load('Recources/Orcs/Walkright/WALK_006.png'),
                                   (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio)))]
orc.idle = [pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_000.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_001.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_002.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_003.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_004.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_005.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Idle/IDLE_006.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio)))]
orc.attackright = [pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_000.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_001.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_002.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_003.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_004.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_005.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackright/ATTAK_006.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio)))]
orc.attackleft = [pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_000.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_001.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_002.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_003.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_004.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_005.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Orcs/Attackleft/ATTAK_006.png'),
                               (int(1686 * scalingfactorx * widthcompratio), int(1234 * scalingfactory * heightcompratio)))]
orc.healthbar = [pygame.transform.scale(pygame.image.load('Recources/Healthbar/1.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/2.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/3.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/4.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/5.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/6.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio))),
        pygame.transform.scale(pygame.image.load('Recources/Healthbar/7.png'),
                               (int(1500 * scalingfactorx * widthcompratio), int(200 * scalingfactory * heightcompratio)))]

bg = pygame.transform.scale(pygame.image.load('Recources/Background/Cartoon_Forest_BG_02.png'),
                            (monitorwidth, monitorheight))

#start menu
menu = True
run = False
victory = False
end = False
menu_font = pygame.font.Font(None, 60)
options = [Option("NEW GAME", (140, 140)), Option("QUIT", (140, 200))]
while menu:
    win.blit(pygame.transform.scale(pygame.image.load('Recources/Background/menu.jpg'),
                            (monitorwidth, monitorheight)), (0, 0))
    pygame.event.pump()
    events = pygame.event.get()
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
            for event in events:
                if event.type == pygame.QUIT:
                    menu = False
                    run = False
                elif (event.type==pygame.MOUSEBUTTONDOWN) and (option.text=="NEW GAME"):
                    menu = False
                    run = True
                elif (event.type==pygame.MOUSEBUTTONDOWN) and (option.text=="QUIT"):
                    menu = False
                    run = False
        else:
            option.hovered = False
        option.draw()
    pygame.display.update()

# mainloop
while run:
    clock.tick(30)

    if heal:
        if mainplayer.health <= 69:
            mainplayer.health += 1
        #print("Healed {}".format(mainplayer.health))
        heal = False
    else:
        if healcount == 10:
            healcount = 0
            heal = True
        else:
            #print(healcount)
            healcount += 1

    count = 0
    #ori = orc.orientation
    if not orc.attack:
        orc.move(orc.x, mainplayer.x)
    else:
        if orc.attackcount + 1 >= 21:
            orc.attack = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_LEFT] and mainplayer.x > mainplayer.vel:
        mainplayer.x -= mainplayer.vel
        mainplayer.weapon.x = mainplayer.x
        mainplayer.body.x = mainplayer.x + 60 * widthcompratio
        mainplayer.left = True
        mainplayer.right = False
        mainplayer.orientation = False
    elif keys[pygame.K_RIGHT] and mainplayer.x < monitorwidth - mainplayer.width - mainplayer.vel:
        mainplayer.x += mainplayer.vel
        mainplayer.weapon.x = mainplayer.x + 160 * widthcompratio
        mainplayer.body.x = mainplayer.x + 10 * widthcompratio
        mainplayer.right = True
        mainplayer.left = False
        mainplayer.orientation = True
    else:
        mainplayer.right = False
        mainplayer.left = False
        mainplayer.orientation = True
        mainplayer.walkCount = 0

    if not mainplayer.attack:
        if keys[pygame.K_SPACE]:
            mainplayer.attackstatus = True
            mainplayer.attack = True
            mainplayer.right = False
            mainplayer.left = False
            mainplayer.walkCount = 0
    else:
        if mainplayer.swordanime <= 8:
            mainplayer.swordanime += 1
        else:
            mainplayer.swordanime = 0
            mainplayer.attack = False

    if not mainplayer.isJump:
        if keys[pygame.K_UP]:
            mainplayer.isJump = True
            mainplayer.right = False
            mainplayer.left = False
            mainplayer.walkCount = 0
    else:
        if mainplayer.jumpCount >= -10:
            mainplayer.y -= (mainplayer.jumpCount * abs(mainplayer.jumpCount)) * 1.5
            mainplayer.weapon.y -= (mainplayer.jumpCount * abs(mainplayer.jumpCount)) * 1.5
            mainplayer.body.y -= (mainplayer.jumpCount * abs(mainplayer.jumpCount)) * 1.5
            mainplayer.vel = 50
            if mainplayer.orientation:
                mainplayer.body.x = mainplayer.x + 30 * widthcompratio
            else:
                mainplayer.body.x = mainplayer.x + 40 * widthcompratio
            mainplayer.jumpCount -= 2
            mainplayer.jumpanime += 1
        else:
            mainplayer.jumpCount = 10
            mainplayer.jumpanime = 0
            mainplayer.isJump = False
            mainplayer.vel = 15

    if not (mainplayer.isJump or mainplayer.left or mainplayer.right or mainplayer.attack):
        mainplayer.weapon.x = mainplayer.x + 160 * widthcompratio
        mainplayer.body.x = mainplayer.x + 10 * widthcompratio
        mainplayer.idlecount += 1
        mainplayer.vel = 15

    orc.damage(mainplayer.weapon, mainplayer.attackstatus)
    mainplayer.damage(orc.weapon, orc.attackstatus)
    if orc.dead or mainplayer.dead:
        if orc.dead:
            victory = True
        run = False
        end = True

    mainplayer.attackstatus = False
    orc.attackstatus = False
    redrawGameWindow()

if end:
    if victory:
        win.blit(pygame.transform.scale(pygame.image.load('Recources/Background/victory.jpg'),
                                        (monitorwidth, monitorheight)), (0, 0))
        menu_font = pygame.font.Font(None, 200)
        vic = Option("VICTORY", (int(monitorwidth*0.35), int(monitorheight*0.4)), (255, 255, 255))
        pygame.display.update()
        sleep(5)
    else:
        win.blit(pygame.transform.scale(pygame.image.load('Recources/Background/defeat.jpg'),
                                        (monitorwidth, monitorheight)), (0, 0))
        menu_font = pygame.font.Font(None, 200)
        vic = Option("DEFEAT", (int(monitorwidth * 0.35), int(monitorheight * 0.4)), (255, 255, 255))
        pygame.display.update()
        sleep(5)

pygame.quit()