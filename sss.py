#Import thư viện hỗ trợ 
from pygame import *
#sử dụng thư viên random 
from random import *
 
 
#GameSprite là class của con sprite.sprite
#sprite.sprite lấy từ thư viện pygame
#GameSprite sẽ được dùng để tạo ra các nhân vật trong game
class GameSprite(sprite.Sprite):
    # hàm khởi tạo
    # luôn phải có từ khóa self
    def __init__(self, character_image, x, y, width, height, speed):
        #kêu cha thực thi trước 
        sprite.Sprite.__init__(self)
        #Tạo ra một cái biến để chứa ảnh của nhân vật 
        self.image = image.load(character_image)
        #phóng to hoặc thu nhỏ ảnh thành kíck thước của  em mong muốn
        self.image = transform.scale(self.image, (width, height))
        # lưu thông tin về tốc độ nhân vật 
        self.speed = speed
 
        #Tạo ra một hình chữ nhật 
        #Biến self.rect chữa hình chữ nhật bằng kích thước tấm ảnh 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #vẽ nhân vật ở tọa độ x, y
        window.blit(self.image,(x, y))
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
 
# Tạo ra class người chơi - class của GameSpite
# Tức là class con có mọi thứ của cha 
class Player(GameSprite):
    #hàm lắng nghe sự điều khiển
    def update(self):
        #lấy ra những nút mới được ấn 
        keys = key.get_pressed()
        # kiểm tra nút vừa ấn 
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    # Hàm bắn đạn
    def fire(self):
        # Tạo ra một cái biến chứa một viên đạn
        bullet = Bullet(img_bullet, x=self.rect.centerx, y=self.rect.top, 
                width=15, height=20, speed=-15)
        bullets.add(bullet)
 
 
# Class viên đạn - con của class GameSprite
class Bullet(GameSprite):
    # Hàm này sẽ cho phép viên đạn di chuyển
    def update(self):
        # Tăng tọa độ y - di chuyển lên trên
        self.rect.y += self.speed
        # Nếu đụng vách trên thì xóa viên đạn
        if self.rect.y < 0:
            self.kill()
 
 
# Class kẻ thù - con của class GameSprite
class Enemy(GameSprite):
    # Hàm di chuyển
    def update(self):
        # Tăng tọa độ y - di chuyển lên trên
        self.rect.y += self.speed
        # Biến đếm số quái vật đã bị bắn hụt
        global lost
        # Nếu con quái vật đụng vách phía trên
        if self.rect.y > win_height:
            # Chọn vị trí ngẫu nhiên mới cho quái vật
            self.rect.x = randint(80, win_widtn - 80)
            self.rect.y = 0
            # Tăng số quái vật bị bắn hụt
            lost = lost + 1
 
 
# Tạo ra một phông chữ dùng để hiện lên màn hình
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
# Viết ra dòng chữ thắng thua
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
 
 
# Tạo ra bộ phát nhạc
mixer.init()
# Load bài nhạc
mixer.music.load('space.ogg')
mixer.music.play()
#  m thanh bắn đạn
fire_sound = mixer.Sound('fire.ogg')
 
# Ảnh cho các nhân vật và vật thể trong game
img_back = "galaxy.jpg" #game background
img_bullet = "bullet.png" #bullet
img_hero = "rocket.png" #hero
img_enemy = "ufo.png" #enemy
 
# Biến chứa điểm
score = 0 # Chưa tiêu diệt kẻ thù nào cả
# Số điểm cần đạt để thắng
goal = 10
# Số điểm cần để thua
lost = 0
# Số điểm tối đa được phép hụt
max_lost = 3
 
# Tạo kích thước màn hình chơi game
win_width = 700
win_height = 500
 
# Đặt tên cho game
display.set_caption('Shooter')
# Tạo ra màn hình với kích thước đã chọn
window = display.set_mode((win_width, win_height))
 
# Hình nền
background = image.load(img_back)
# Phóng to/thu nhỏ tấm hình cho vừa màn hình game
background = transform.scale(background, (win_width, win_height))
 
# Tạo ra phi thuyền
ship = Player(img_hero, x=5, y=win_height-100, width=80, height=100, speed=10)
 
# Tạo ra một nhóm các con quái vật
monsters = sprite.Group()
 
# Tạo ra 6 con quái vật sử dụng vòng lặp
for i in range(1, 6):
    monster = Enemy(img_enemy, x=randint(80, win_width - 80), y=-40, width=80, height=50, speed=3)
    monsters.add(monster)
 
# Danh sách những viên đạn
bullets = sprite.Group()
# Tạo ra một biến tính xem game kết thúc chưa
finish = False
# Tạo biến kiểm tra coi game có đang chạy không
run = True
 
 
# Trong khi game còn đang chạy
while run:
    # Trong tất cả các hoạt động đang diễn ra
    for e in event.get():
        # Kiểm tra xem có tắt game không
        if e.type == QUIT:
            run = False
        # Bắn đạn
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # Bắn đạn
                # Kích hoạt âm thanh
                fire_sound.play()
                # Cho phi thuyền bắn đạn
                ship.fire()
 
    if not finish:
        # Cập nhật lại hình nền
        window.blit(background, (0, 0))
 
        # Cập nhật chuyển động cho game
        ship.update()
        monsters.update()
        bullets.update()
 
        ship.reset()
 
        # Vẽ những con quái vật lên màn hình
        monsters.draw(window)
        bullets.draw(window)
 
        # Kiểm tra coi viên đạn nào bắn trúng
        collides = sprite.groupcollide(monsters, bullets, True, True)
 
        for c in collides:
            score += 1
            monster = Enemy(img_enemy,
                x=randint(80, win_width - 80),
                y=-40,
                width=80,
                height=50, 
                speed=randint(1, 5))
 
            monsters.add(monster)
 
        # Bắn hụt quá nhiều con quái vật
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
 
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
 
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 20))
 
        # Cập nhật màn hình game sau mỗi giây
        display.update()
    else:
        finish = True
        score = 0
        lost = 0
        for bullet in bullets:
            bullet.kill()
 
        for monster in monsters:
            monster.kill()
 
        time.delay(3000)
    
    time.delay(50)
