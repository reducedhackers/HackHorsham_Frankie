#  thanks to https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer for pyscope
#   


import pygame
import time
import datetime
import random
import RPi.GPIO as GPIO
import os


GPIO.setmode(GPIO.BCM)
startbutton=26
tweezers=19
GPIO.setup(startbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tweezers, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class pyscope :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
 
    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

    def resetscreen(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        black = (0, 0, 0)
        self.screen.fill(black)
        # Update the display
        pygame.display.update()

    def gameend(self):
	self.resetscreen()
	myfont = pygame.font.SysFont("monospace", 248)
	label = myfont.render(" GAME END  ", 1, (255,255,0))
        self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
        pygame.display.update()
        time.sleep(10)

    def gamestop(self):
	self.resetscreen()
	myfont = pygame.font.SysFont("monospace", 248)
	label = myfont.render(" GAME OVER  ", 1, (255,255,0))
        self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
        pygame.display.update()
        time.sleep(10)

    def playgame(self):
        self.resetscreen()
        myfont = pygame.font.SysFont("monospace", 124)
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=60)
        startTime = datetime.datetime.now()
        nowTime  = datetime.datetime.now()
        counter = endTime - nowTime
        while True:
                lastcount = counter
                nowTime  = datetime.datetime.now()
                counter = endTime - nowTime
                gameStop = False
                if datetime.datetime.now() >= endTime:
                        gameStop = False
                        break
                label = myfont.render( str(counter)  , 1, (255,255,0))
                blank = myfont.render( str(lastcount)  , 1, (0,0,0))
                self.screen.blit(blank,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
                self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
                pygame.display.update()

		input_state = GPIO.input(26) 
		if input_state == False:
			self.gamehalt(counter)
			break

                input_state = GPIO.input(19)
                if input_state == False:
                        self.gamestop()
                        gameStop = True
                        break
        if gameStop == False:
                self.gameend()

    def gamehalt(counter):
	self.resetscreen()
 	myfont = pygame.font.SysFont("monospace", 124)
	label = myfont.render( "Your Time was " + str(counter)  , 1, (255,255,0))
        self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
        pygame.display.update()
	while True:
		input_state = GPIO.input(26) 
		if input_state == False:
			break
	 

    def countdown(self):
	self.resetscreen()
 	myfont = pygame.font.SysFont("monospace", 124)
	for cdown in range(3,0,-1):
		self.resetscreen()
       		label = myfont.render( str(cdown)  , 1, (255,255,0))
        	self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
       		pygame.display.update()
		time.sleep(1)


    def newgame(self):
	self.resetscreen()
	myfont = pygame.font.SysFont("monospace", 124)
       	label = myfont.render(" NEW GAME ", 1, (255,255,0))
        self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
       	pygame.display.update()
	time.sleep(3)

    def pressbutton(self):
	self.resetscreen()
	myfont = pygame.font.SysFont("monospace", 124)
       	label = myfont.render(" PRESS EASY TO BEGIN ", 1, (255,255,0))
        self.screen.blit(label,((pygame.display.Info().current_w - label.get_width())/2,( pygame.display.Info().current_h  - label.get_height() ) /2  ))
       	pygame.display.update()


# Create an instance of the PyScope class
scope = pyscope()


while True:
	input_state = GPIO.input(startbutton) 
	if input_state == False:
		scope.newgame()
		scope.countdown()
		scope.playgame()
				
	else :
		scope.pressbutton()
		time.sleep(2)
