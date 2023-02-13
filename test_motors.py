# import curses and GPIO
import curses
import RPi.GPIO as GPIO

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)      # motor A (right)    -> forwards    (M1)
GPIO.setup(11,GPIO.OUT)     # motor A (left)     -> backwards   (E1)
GPIO.setup(13,GPIO.OUT)     # motor B  (right)   -> forwards    (M2)
GPIO.setup(15,GPIO.OUT)     # motor B  (left)    -> backwards   (E2)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr() 
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
        while True:   
            char = screen.getch()
            if char == ord('q'):
                break
            if char == ord('S'):
                os.system('sudo shutdown now')
            # both motors backwards (forwards)
            elif char == curses.KEY_DOWN:
                GPIO.output(7,False) # M1
                GPIO.output(11,True) # E1

                GPIO.output(13,False) # M2
                GPIO.output(15,True) # E2
            # both motors forwards (backwards)
            elif char == curses.KEY_UP:
                GPIO.output(7,True)
                GPIO.output(11,True)

                GPIO.output(13,True)
                GPIO.output(15,True)
            # right forwards, left backwards (turning left)
            elif char == curses.KEY_LEFT:
                GPIO.output(7,False)
                GPIO.output(11,True)

                GPIO.output(13,True)
                GPIO.output(15,False)
            # right backwards, left forwards (turning right)
            elif char == curses.KEY_RIGHT:
                GPIO.output(7,True)
                GPIO.output(11,False)

                GPIO.output(13,False)
                GPIO.output(15,True)
            # stop motors
            elif char == ord('x'):
                GPIO.output(7,False)
                GPIO.output(11,False)

                GPIO.output(13,False)
                GPIO.output(15,False)
            elif char == ord('m'):
                GPIO.output(7,False)
                GPIO.output(11,False)

                GPIO.output(13,False)
                GPIO.output(15,True)
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    
