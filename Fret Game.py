__author__ = 'gregory'

import pygame
import random

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.offwhite = (252,233,201)
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image,self.offwhite,[0,0,width,height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height



    def text_objects(self,text,font):
        textsurface = font.render(text,True,(0,0,0))
        return textsurface, textsurface.get_rect()

    def update(self,msg):
        pygame.draw.rect(self.image,self.offwhite,[0,0,self.width,self.height])
        self.msg = msg
        self.font = pygame.font.Font("freesansbold.ttf",20)
        self.textSurf, self.textRect = self.text_objects(self.msg,self.font)
        self.textRect.center = (self.width/2,self.height/2)
        self.image.blit(self.textSurf, self.textRect)


class Game(object):
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.offwhite = (252,233,201)
        self.strings = ["d1", "a", "e", "c", "g", "d"]
        self.string_pos = {"d1": [98,174,113,659],
                           "a": [93,174,102,659],
                           "e": [87,174,92,659],
                           "c": [81,174,78,659],
                           "g": [75,174,65,659],
                           "d": [68,174,55,659]}
        self.frets = [0,1,2,3,4,5,6,7]
        self.fret_pos = {0: [63,174,101,174],
                         1: [60,195,106,195],
                         2: [59,216,107,216],
                         3: [58,237,108,237],
                         4: [57,258,109,258],
                         5: [56,279,110,279],
                         6: [56,300,111,300],
                         7: [55,321,112,321]}
        self.notes = {}
        self.note_names = ["A","Bb","B","C","C#","D","D#/Eb","E","F","F#","G","G#/Ab"]

        for string in self.strings:
            if string == "d1":
                start_note = 5
            elif string == "a":
                start_note = 0
            elif string == "e":
                start_note = 7
            elif string == "c":
                start_note = 3
            elif string == "g":
                start_note = 10
            elif string == "d":
                start_note = 5

            for fret in self.frets:
                self.notes[(string,fret)] = self.note_names[start_note]
                if start_note < 11:
                    start_note += 1
                else:
                    start_note = 0

        self.answerset = ()

    def pick_answer(self):
        stringchoice = random.choice(self.strings)
        fretchoice = random.choice(self.frets)
        answer =  self.notes[(stringchoice,fretchoice)]
        choices = [answer]
        note_list = list(self.notes.values())
        counter = 0
        while counter < 3:
            note = random.choice(note_list)
            if note != answer and note not in choices:
                choices.append(note)
                counter += 1
        random.shuffle(choices)
        return stringchoice, fretchoice, answer, choices

    def fret(self, startx, starty, endx, endy, thickness, fret_num):
        if fret_num == 0:
            pygame.draw.lines(screen, self.black, False, [(startx, starty), (endx,endy)], thickness)
        elif self.answerset[1] == fret_num:
            pygame.draw.lines(screen, self.red, False, [(startx, starty), (endx,endy)], thickness)
        else:
            pygame.draw.lines(screen, self.offwhite, False, [(startx, starty), (endx,endy)], thickness)


    def string(self, startx, starty, endx, endy, thickness, str_name):
        if self.answerset[0] == str_name:
            pygame.draw.lines(screen, self.red, True, [(startx, starty), (endx,endy)], thickness)
        else:
            pygame.draw.lines(screen, self.offwhite, True, [(startx, starty), (endx,endy)], thickness)


    def display_response(self,response):
        render_text = self.font.render(response,True,(0,0,0))
        return render_text

    def main(self, screen):
        button_list = pygame.sprite.Group()
        print(button_list)
        self.answerset = self.pick_answer()
        self.choices = self.answerset[3]
        button1 = Button(300,150,70,50)
        button2 = Button(300,220,70,50)
        button3 = Button(300,290,70,50)
        button4 = Button(300,360,70,50)
        button_list.add(button1)
        button_list.add(button2)
        button_list.add(button3)
        button_list.add(button4)
        button1.update(self.choices[0])
        button2.update(self.choices[1])
        button3.update(self.choices[2])
        button4.update(self.choices[3])
        clock = pygame.time.Clock()
        background = pygame.image.load("Violcropped.png").convert()
        self.font = pygame.font.SysFont("vivaldi",40)
        self.response_text = ""
        self.response = self.font.render(self.response_text,True,(0,0,0))
        self.time_to_blit = None
        pygame.display.set_caption("Viola da Gamba")
        pygame.display.set_icon(pygame.image.load('F3.png'))
        while 1:
            clock.tick(30)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONUP:
                    x,y = event.pos
                    for button in button_list:
                        if button.rect.collidepoint(x,y):
                            self.time_to_blit = pygame.time.get_ticks() + 1500
                            if button.msg == self.answerset[2]:
                                self.answerset = self.pick_answer()
                                self.choices = self.answerset[3]
                                button1.update(self.choices[0])
                                button2.update(self.choices[1])
                                button3.update(self.choices[2])
                                button4.update(self.choices[3])
                                self.response_text = "Correct"

                            elif button.msg != self.answerset[2]:
                                self.answerset = self.pick_answer()
                                self.choices = self.answerset[3]
                                button1.update(self.choices[0])
                                button2.update(self.choices[1])
                                button3.update(self.choices[2])
                                button4.update(self.choices[3])
                                self.response_text = "Wrong"
                                #self.response = self.font.render("Wrong",True,(0,0,0))

            screen.blit(background,(0,0))
            for key in self.fret_pos:
                x = self.fret_pos[key]
                self.fret(x[0], x[1], x[2], x[3], 2, key)

            for key in self.string_pos:
                x = self.string_pos[key]
                self.string(x[0],x[1],x[2],x[3],1,key)

            if self.time_to_blit:
                screen.blit(self.display_response(self.response_text),(280,10))
                if pygame.time.get_ticks() >= self.time_to_blit:
                    self.time_to_blit = None
            button_list.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((427, 700))
    Game().main(screen)
