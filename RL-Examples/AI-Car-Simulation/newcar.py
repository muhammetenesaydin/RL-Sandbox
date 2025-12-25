# Bu kod, YouTuber Cheesy AI'dan büyük ölçüde esinlenmiştir.
# Kod Değiştirildi, Optimize Edildi ve Yorumlandı: NeuralNine (Florian Dedov)
# Türkçe Açıklamalar Ekleyen: AI Asistan

import math
import random
import sys
import os

import neat
import pygame

# Sabit Değerler
# WIDTH = 1600
# HEIGHT = 880

WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 60    
CAR_SIZE_Y = 60

BORDE_COLOR = (255, 255, 255, 255) # Arabanın çarptığında öleceği sınır rengi (Beyaz)

current_generation = 0 # Nesil sayacı

class Car:

    def __init__(self):
        # Araba görselini yükle ve ölçeklendir
        self.sprite = pygame.image.load('car.png').convert() # .convert() işlemi işlemleri çok hızlandırır
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 

        # Başlangıç Pozisyonu
        # self.position = [690, 740]
        self.position = [830, 920]
        self.angle = 0
        self.speed = 0

        self.speed_set = False # Varsayılan hızın ayarlanıp ayarlanmadığını kontrol eden bayrak

        # Arabanın merkez noktasını hesapla
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]

        self.radars = [] # Sensörlerden (radarlar) gelen verilerin listesi
        self.drawing_radars = [] # Ekrana çizilecek olan radarlar

        self.alive = True # Arabanın çarpıp çarpmadığını kontrol eden değişken

        self.distance = 0 # Gidilen toplam mesafe
        self.time = 0 # Geçen toplam süre

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position) # Arabayı ekrana çiz
        self.draw_radar(screen) # İsteğe bağlı: Sensörleri (radarları) görselleştir

    def draw_radar(self, screen):
        # Tüm sensörleri / radarları ekrana çiz
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1) # Yeşil çizgi
            pygame.draw.circle(screen, (0, 255, 0), position, 5) # Çizgi ucundaki nokta

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            # Arabanın herhangi bir köşesi sınır rengine (beyaz) değerse -> Kaza yap
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDE_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        length = 0
        # Radarın başlangıç noktası (merkezden başlar)
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Sınır rengine çarpmadığımız sürece ve uzunluk 300'den küçükse ilerle
        while not game_map.get_at((x, y)) == BORDE_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Sınıra olan mesafeyi hesapla ve radarlar listesine ekle
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map):
        # İlk başlangıçta hızı 20 olarak ayarla (sadece bir kez çalışır)
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Arabayı döndür ve açısına göre hareket ettir
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        
        # Arabanın ekran dışına çıkmasını engelle (X ekseni)
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Mesafe ve zamanı artır
        self.distance += self.speed
        self.time += 1
        
        # Y ekseni için hareket ve sınır kontrolü
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Yeni merkez noktasını hesapla
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Arabanın dört köşesini hesapla (çarpışma kontrolü için)
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Çarpışmaları kontrol et ve radarları temizle
        self.check_collision(game_map)
        self.radars.clear()

        # -90'dan 120 dereceye kadar 45'er derece aralıkla 5 adet radar kontrolü yap
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        # Sınırlara olan mesafeleri al ve normalleştirerek sinir ağına gönder
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        # Arabanın hayatta olup olmadığını döndürür
        return self.alive

    def get_reward(self):
        # Fitness (başarı) puanını hesapla: Gidilen mesafe ödül olarak döner
        return self.distance / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        # Görseli merkezinden döndürmeyi sağlayan yardımcı fonksiyon
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image


def run_simulation(genomes, config):
    
    # Sinir ağları ve araba nesneleri için boş listeler
    nets = []
    cars = []

    # PyGame'i başlat ve ekranı ayarla
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # Her bir genom (yapay zeka adayı) için bir sinir ağı ve araba oluştur
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0 # Başlangıç fitness puanı

        cars.append(Car())

    # Saat, yazı tipi ve harita ayarları
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('map5.png').convert() # Harita dosyasını yükle

    global current_generation
    current_generation += 1

    # Zamanı kabaca sınırlamak için bir sayaç
    counter = 0

    while True:
        # Çıkış işlemi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # Her bir araba için sinir ağından gelen kararları uygula
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10 # Sola dön
            elif choice == 1:
                car.angle -= 10 # Sağa dön
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2 # Yavaşla
            else:
                car.speed += 2 # Hızlan
        
        # Arabaların hayatta olup olmadığını kontrol et
        # Hayattaysa fitness puanını artır, değilse döngüden çık
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        # Eğer hiç araba kalmadıysa bu nesli bitir
        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40: # Yaklaşık 20 saniye sonra nesli sonlandır (Sonsuz döngüyü önlemek için)
            break

        # Haritayı ve hayatta kalan arabaları çiz
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)
        
        # Ekran üzerine güncel nesil ve hayatta kalan araba sayısını yaz
        text = generation_font.render("Nesil: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Hayatta Kalan: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60) # Saniyede 60 kare (FPS)

if __name__ == "__main__":
    
    # NEAT Yapılandırma dosyasını yükle
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Popülasyonu oluştur ve raporlayıcıları ekle (konsol çıktısı ve istatistikler için)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Simülasyonu maksimum 1000 nesil boyunca çalıştır
    population.run(run_simulation, 1000)
