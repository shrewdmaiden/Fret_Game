__author__ = 'gregory'

import pygame
import random

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
        self.frets = [0,1]
        self.fret_pos = {0: [65,174,102,174],
                         1: [65,195,102,195]}
        self.notes = {("d",0): "D",
                      ("a",0): "A",
                      ("e",0): "E",
                      ("c",0): "C",
                      ("g",0): "G",
                      ("d1",0): "D",
                      ("d", 1): "D#",
                      ("a",1): "Bb",
                      ("e",1): "F",
                      ("c",1): "C#",
                      ("g",1): "G#",
                      ("d1",1): "D#"}
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



    def text_objects(self,text,font):
        textsurface = font.render(text,True,self.black)
        return textsurface, textsurface.get_rect()

    def display_response(self,response):
        smallText = pygame.font.SysFont("vivaldi",40)
        textSurf, textRect = self.text_objects(response,smallText)
        textRect.center = (327,50)
        screen.blit(textSurf,textRect)

    def button(self,msg,x,y,width,height):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x+(width/2)),(y+(height/2)))
        pygame.draw.rect(screen,self.offwhite,(x, y, width, height))
        screen.blit(textSurf, textRect)
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            if click[0] == 1:
                if msg == self.answerset[2]:
                    self.display_response("correct")
                elif msg != self.answerset[2]:
                    self.display_response("wrong")
                self.answerset = self.pick_answer()

    def fret(self, startx, starty, endx, endy, thickness, fret_num):
        if self.answerset[1] == fret_num:
            pygame.draw.lines(screen, self.red, False, [(startx, starty), (endx,endy)], thickness)
        else:
            pygame.draw.lines(screen, self.offwhite, False, [(startx, starty), (endx,endy)], thickness)


    def string(self, startx, starty, endx, endy, thickness, str_name):
        if self.answerset[0] == str_name:
            pygame.draw.lines(screen, self.red, False, [(startx, starty), (endx,endy)], thickness)
        else:
            pygame.draw.lines(screen, self.offwhite, False, [(startx, starty), (endx,endy)], thickness)


    def main(self, screen):
        clock = pygame.time.Clock()
        self.answerset = self.pick_answer()
        background = pygame.image.load("Violcropped.png")
        while 1:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            screen.blit(background,(0,0))

            for key in self.string_pos:
                x = self.string_pos[key]
                self.string(x[0],x[1],x[2],x[3],1,key)

            for key in self.fret_pos:
                x = self.fret_pos[key]
                self.fret(x[0], x[1], x[2], x[3], 2, key)

            button_start = 100
            for i in self.answerset[3]:
                self.button(i,300,button_start,50,50)
                button_start += 70

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((427, 700))
    Game().main(screen)
