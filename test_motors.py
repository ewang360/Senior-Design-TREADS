# import curses and GPIO
import curses
import RPi.GPIO as GPIO

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)      # motor A (right)   -> forwards
GPIO.setup(11,GPIO.OUT)     # motor A (right)   -> backwards
GPIO.setup(13,GPIO.OUT)     # motor B  (left)   -> forwards
GPIO.setup(15,GPIO.OUT)     # motor B  (left)    -> backwards

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
            # both motors backwards (backwards)
            elif char == curses.KEY_DOWN:
                GPIO.output(7,False)
                GPIO.output(11,True)
                GPIO.output(13,False)
                GPIO.output(15,True)
            # both motors forwards (forwards)
            elif char == curses.KEY_UP:
                GPIO.output(7,True)
                GPIO.output(11,False)
                GPIO.output(13,True)
                GPIO.output(15,False)
            # right backwards, left forwards (turning left)
            elif char == curses.KEY_LEFT:
                GPIO.output(7,True)
                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(15,True)
            # right forwards, left backwards (turning right)
            elif char == curses.KEY_RIGHT:
                GPIO.output(7,False)
                GPIO.output(11,True)
                GPIO.output(13,True)
                GPIO.output(15,False)
            # stop motors
            elif char == 'x':
                GPIO.output(7,False)
                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(15,False)
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    
