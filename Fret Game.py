__author__ = 'gregory'

import pygame
import random

class Game(object):
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.strings = ["d1", "a", "e", "c", "g", "d"]
        self.frets = [0,1]
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

    def button(self,msg,x,y,width,height):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x+(width/2)),(y+(height/2)))
        pygame.draw.rect(screen,self.red,(x, y, width, height))
        screen.blit(textSurf, textRect)
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            if click[0] == 1:
                if msg == self.answerset[2]:
                    print("Yay!")
                else:
                    print("wrong")
                self.answerset = self.pick_answer()

    def fret(self, startx, starty, endx, endy, thickness, fret_num):
        if self.answerset[1] == fret_num:
            pygame.draw.lines(screen, self.red, False, [(startx, starty), (endx,endy)], thickness)
        else:
            pygame.draw.lines(screen, self.black, False, [(startx, starty), (endx,endy)], thickness)


    def string(self, startx, starty, endx, endy, thickness, str_name):
        if self.answerset[0] == str_name:
            pygame.draw.lines(screen, self.red, False, [(startx, starty), (endx,endy)], thickness)
        else:
            pygame.draw.lines(screen, self.black, False, [(startx, starty), (endx,endy)], thickness)


    def main(self, screen):
        clock = pygame.time.Clock()
        self.answerset = self.pick_answer()
        while 1:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            screen.fill(self.white)

            string_start = 50
            for i in self.strings:
                self.string(10,string_start,990,string_start,5,i)
                string_start += 40

            fret_start = 10
            for i in self.frets:
                self.fret(fret_start, 50, fret_start, 250, 5, i)
                fret_start += 60

            button_start = 200
            for i in self.answerset[3]:
                self.button(i,button_start,450,50,50)
                button_start += 70

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    Game().main(screen)
