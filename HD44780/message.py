from hd44780 import HD44780
import sys

lcd = HD44780()
delay = float(sys.argv[2]) if len(sys.argv) > 2 else 0
lcd.message(sys.argv[1], delay)
