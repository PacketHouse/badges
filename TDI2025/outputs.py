# Author: str3tch @ Vegas 2.0 | dc702 / @JustJeromy
# Description: Handles all the output stuff (screen, leds, etc.)
# Other Credits: Some of the base code came from
#                The Diana Initiative Maker Village (thanks, Chris & Liam)
import array
import framebuf
import random
import rp2
import sys
import time
import utime

from machine import ADC, I2C, Pin, I2C, ADC
from picozero import LED
from ssd1306 import SSD1306_I2C


DEFAULT_BRIGHTNESS = 0.5
DEFAULT_COLOR = 'RED'
DEFAULT_WAIT = 0.5

PronounColors = {'SHE': 'DEEP PINK',
                 'HE': 'BLUE',
                 'MANY': 'WHITE',
                 'MIXED': 'PURPLE',
                 'NONBINARY': 'GREEN',
                 'NONE': 'BLACK',
                 'THEY': 'YELLOW'}

DarkColors = ['DARK BLUE',
              'DARK CYAN',
              'DARK GOLDEN ROD',
              'DARK GRAY',
              'DARK GREEN',
              'DARK KHAKI',
              'DARK MAGENTA',
              'DARK OLIVE GREEN',
              'DARK ORANGE',
              'DARK ORCHID',
              'DARK RED',
              'DARK SALMON',
              'DARK SEA GREEN',
              'DARK SLATE BLUE',
              'DARK SLATE GRAY',
              'DARK TURQUOISE',
              'DARK VIOLET']

SimpleColors = ['DARK BLUE', ' DARK GREEN', 'PURPLE', 'RED']

Colors = {'ALICE BLUE': (240, 248, 255),
          'ANTIQUE WHITE': (250, 235, 215),
          'AQUA': (0, 255, 255),
          'AQUA MARINE': (127, 255, 212),
          'AZURE': (240, 255, 255),
          'BEIGE': (245, 245, 220),
          'BISQUE': (255, 228, 196),
          'BLACK': (0, 0, 0),
          'BLANCHED ALMOND': (255, 235, 205),
          'BLUE': (0, 0, 255),
          'BLUE VIOLET': (138, 43, 226),
          'BROWN': (165, 42, 42),
          'BURLY WOOD': (222, 184, 135),
          'CADET BLUE': (95, 158, 160),
          'CHARTREUSE': (127, 255, 0),
          'CHOCOLATE': (210, 105, 30),
          'CORAL': (255, 127, 80),
          'CORN FLOWER BLUE': (100, 149, 237),
          'CORN SILK': (255, 248, 220),
          'CRIMSON': (220, 20, 60),
          'CYAN': (0, 255, 255),
          'DARK BLUE': (0, 0, 139),
          'DARK CYAN': (0, 139, 139),
          'DARK GOLDEN ROD': (184, 134, 11),
          'DARK GRAY': (169, 169, 169),
          'DARK GREY': (169, 169, 169),
          'DARK GREEN': (0, 100, 0),
          'DARK KHAKI': (189, 183, 107),
          'DARK MAGENTA': (139, 0, 139),
          'DARK OLIVE GREEN': (85, 107, 47),
          'DARK ORANGE': (255, 140, 0),
          'DARK ORCHID': (153, 50, 204),
          'DARK RED': (139, 0, 0),
          'DARK SALMON': (233, 150, 122),
          'DARK SEA GREEN': (143, 188, 143),
          'DARK SLATE BLUE': (72, 61, 139),
          'DARK SLATE GRAY': (47, 79, 79),
          'DARK TURQUOISE': (0, 206, 209),
          'DARK VIOLET': (148, 0, 211),
          'DEEP PINK': (255, 20, 147),
          'DEEP SKY BLUE': (0, 191, 255),
          'DIM GRAY': (105, 105, 105),
          'DIM GREY': (105, 105, 105),
          'DODGER BLUE': (30, 144, 255),
          'FIREBRICK': (178, 34, 34),
          'FLORAL WHITE': (255, 250, 240),
          'FOREST GREEN': (34, 139, 34),
          'GAINSBORO': (220, 220, 220),
          'GHOST WHITE': (248, 248, 255),
          'GOLD': (255, 215, 0),
          'GOLDEN ROD': (218, 165, 32),
          'GRAY': (128, 128, 128),
          'GREY': (128, 128, 128),
          'GREEN': (0, 128, 0),
          'GREEN YELLOW': (173, 255, 47),
          'HONEYDEW': (240, 255, 240),
          'HOT PINK': (255, 105, 180),
          'INDIAN RED': (205, 92, 92),
          'INDIGO': (75, 0, 130),
          'IVORY': (255, 255, 240),
          'KHAKI': (240, 230, 140),
          'LAVENDER': (230, 230, 250),
          'LAVENDER BLUSH': (255, 240, 245),
          'LAWN GREEN': (124, 252, 0),
          'LEMON CHIFFON': (255, 250, 205),
          'LIGHT BLUE': (173, 216, 230),
          'LIGHT CORAL': (240, 128, 128),
          'LIGHT CYAN': (224, 255, 255),
          'LIGHT GOLDEN ROD YELLOW': (250, 250, 210),
          'LIGHT GRAY': (211, 211, 211),
          'LIGHT GREY': (211, 211, 211),
          'LIGHT GREEN': (144, 238, 144),
          'LIGHT PINK': (255, 182, 193),
          'LIGHT SALMON': (255, 160, 122),
          'LIGHT SEA GREEN': (32, 178, 170),
          'LIGHT SKY BLUE': (135, 206, 250),
          'LIGHT SLATE GRAY': (119, 136, 153),
          'LIGHT STEEL BLUE': (176, 196, 222),
          'LIGHT YELLOW': (255, 255, 224),
          'LIME': (0, 255, 0),
          'LIME GREEN': (50, 205, 50),
          'LINEN': (250, 240, 230),
          'MAGENTA': (255, 0, 255),
          'FUCHSIA': (255, 0, 255),
          'MAROON': (128, 0, 0),
          'MEDIUM AQUA MARINE': (102, 205, 170),
          'MEDIUM BLUE': (0, 0, 205),
          'MEDIUM ORCHID': (186, 85, 211),
          'MEDIUM PURPLE': (147, 112, 219),
          'MEDIUM SEA GREEN': (60, 179, 113),
          'MEDIUM SLATE BLUE': (123, 104, 238),
          'MEDIUM SPRING GREEN': (0, 250, 154),
          'MEDIUM TURQUOISE': (72, 209, 204),
          'MEDIUM VIOLET RED': (199, 21, 133),
          'MIDNIGHT BLUE': (25, 25, 112),
          'MINT CREAM': (245, 255, 250),
          'MISTY ROSE': (255, 228, 225),
          'MOCCASIN': (255, 228, 181),
          'NAVAJO WHITE': (255, 222, 173),
          'NAVY': (0, 0, 128),
          'OLD LACE': (253, 245, 230),
          'OLIVE': (128, 128, 0),
          'OLIVE DRAB': (107, 142, 35),
          'ORANGE': (255, 165, 0),
          'ORANGE RED': (255, 69, 0),
          'ORCHID': (218, 112, 214),
          'PALE GOLDEN ROD': (238, 232, 170),
          'PALE GREEN': (152, 251, 152),
          'PALE TURQUOISE': (175, 238, 238),
          'PALE VIOLET RED': (219, 112, 147),
          'PAPAYA WHIP': (255, 239, 213),
          'PEACH PUFF': (255, 218, 185),
          'PERU': (205, 133, 63),
          'PINK': (255, 192, 203),
          'PLUM': (221, 160, 221),
          'POWDER BLUE': (176, 224, 230),
          'PURPLE': (128, 0, 128),
          'RED': (255, 0, 0),
          'ROSY BROWN': (188, 143, 143),
          'ROYAL BLUE': (65, 105, 225),
          'SADDLE BROWN': (139, 69, 19),
          'SALMON': (250, 128, 114),
          'SANDY BROWN': (244, 164, 96),
          'SEA GREEN': (46, 139, 87),
          'SEA SHELL': (255, 245, 238),
          'SIENNA': (160, 82, 45),
          'SILVER': (192, 192, 192),
          'SKY BLUE': (135, 206, 235),
          'SLATE BLUE': (106, 90, 205),
          'SLATE GRAY': (112, 128, 144),
          'SNOW': (255, 250, 250),
          'SPRING GREEN': (0, 255, 127),
          'STEEL BLUE': (70, 130, 180),
          'TAN': (210, 180, 140),
          'TEAL': (0, 128, 128),
          'THISTLE': (216, 191, 216),
          'TOMATO': (255, 99, 71),
          'TURQUOISE': (64, 224, 208),
          'VIOLET': (238, 130, 238),
          'WHEAT': (245, 222, 179),
          'WHITE': (255, 255, 255),
          'WHITE SMOKE': (245, 245, 245),
          'YELLOW': (255, 255, 0),
          'YELLOW GREEN': (154, 205, 50)}


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label('bitloop')
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, 'do_zero').side(1)[T1 - 1]
    jmp('bitloop').side(1)[T2 - 1]
    label('do_zero')
    nop().side(0)[T2 - 1]
    wrap()


class LedShow(object):
    def __init__(self, pins=[14, 15]):
        self.leds = []
        for pin in pins:
            led = LED(pin)
            led.on()
            self.leds.append(led)

    def clear(self):
        for led in self.leds:
            led.off()

    def get_leds(self):
        return self.leds

    def set_on(self, num=-1, wait=0):
        # default to all LEDs
        if num < 0 or num >= len(self.leds):
            leds = self.leds
        else:
            leds = [self.leds[num]]

        for led in leds:
            led.on()
            time.sleep(wait)

    def pulse(self, fade_in_time=1, fade_out_time=None, count=5, num=-1,
              wait=DEFAULT_WAIT / 2, fps=25):
        # default to all LEDs
        if num < 0 or num >= len(self.leds):
            leds = self.leds
        else:
            leds = [self.leds[num]]

        for i in range(count):
            for led in leds:
                led.pulse(fade_in_time, fade_out_time, count, False, fps)
                time.sleep(wait)

    def toggle(self, num=-1, wait=DEFAULT_WAIT, choose_random=False):
        if choose_random:
            num = random.randint(0, len(self.leds) - 1)

        # default to all LEDs
        if num < 0 or num >= len(self.leds):
            leds = self.leds
        else:
            leds = [self.leds[num]]

        for led in leds:
            led.toggle()
            time.sleep(wait)


class OledShow(object):
    def __init__(self, res_x=128, res_y=32, scl_pin=27, sda_pin=26,
                 lds=None, pxs=None):
        self.res_x = res_x
        self.res_y = res_y

        i2c_dev = self.init_i2c(scl_pin, sda_pin)
        self.oled = SSD1306_I2C(res_x, res_y, i2c_dev)

        # Allow OledShow to interact with LedShow and PixelShow objects
        # for more fun
        self.lds = lds
        self.pxs = pxs

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def draw_pixels(self, pixels, clear=True):
        # Make sure we start with a blank slate
        if clear:
            self.clear()

        for i in range(len(pixels)):
            if pixels[i] == 1:
                y = int(i / self.res_x)
                x = int(i % self.res_x)
                self.oled.pixel(x, y, 1)

        self.oled.show()

    def init_i2c(self, scl_pin, sda_pin):
        # Initialize I2C device
        i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
        i2c_addr = [hex(ii) for ii in i2c_dev.scan()]

        if not i2c_addr:
            print('No I2C Display Found')
            sys.exit()
        else:
            print(f'I2C Address      : {i2c_addr[0]}')
            print(f'I2C Configuration: {i2c_dev}')
            pass

        return i2c_dev

    def show_company(self, company='', split_name=True):
        self.clear()
        if split_name:
            company_parts = company.split()
            y = 5
            for part in company_parts:
                self.oled.text(part, 5, y)
                y += 10
        else:
            self.oled.text(company, 5, 5)
        self.oled.show()

    def show_handle(self, name='nobody'):
        self.clear()
        self.oled.text('My friends', 5, 5)
        self.oled.text('call me', 5, 15)
        self.oled.text(f'{name}', 5, 25)
        self.oled.show()

    def show_moving_ball(self, wait=0):
        self.clear()

        dx = 1  # Initial directions
        dy = 1
        x = 13  # Start position of ball
        y = 20
        # ols.oled.rect(0,0,ols.res_x,ols.res_y,1)    # Draw edges once

        for loop in range(218):
            self.oled.ellipse(x, y, 5, 5, 1, 1)  # Filled circle
            self.oled.show()  # Update changes
            self.oled.ellipse(x, y, 5, 5, 0, 1)  # Filled circle - rubout
            x = x + dx
            y = y + dy

            # Reverse direction after hitting the right or left wall
            if (x == self.res_x - 5) or (x == 5):
                # Reverse x direction
                dx = dx * -1

                # Do blinky things
                self.lds.toggle(wait=wait, choose_random=True)

            # Reverse direction after hitting the ceiling or floor
            if (y == self.res_y - 5) or (y == 5):
                dy = dy * -1  # Reverse y direction

                # Do blinky things
                if self.pxs:
                    self.pxs.set_pixel(0, 'red', wait=wait)
                    self.pxs.set_pixel(1, 'green', wait=wait)
                    self.pxs.set_pixel(2, 'blue', wait=wait)
                    self.pxs.show_pixels(brightness=0.25, wait=wait)

                if self.lds:
                    self.lds.toggle(wait=0, choose_random=True)

    def show_moving_text(self, text='ping', wait=0.05):
        self.clear()

        # Initial directions
        dx = 1
        dy = 1

        # Start position for text
        x = 0
        y = 0

        # Text dimensions (8x8 pixels per character)
        ty = 8
        tx = len(text) * 8

        for loop in range(self.res_x + self.res_y - 8):
            self.clear()
            self.oled.text(text, x, y, 1)
            self.oled.show()

            # Move text
            x = x + dx
            y = y + dy

            # Do blinky stuff too
            if self.lds:
                # Change a random LED once in a while
                if loop % tx == 0:
                    self.lds.toggle(choose_random=True, wait=wait)

            if self.pxs:
                # Change a random RGB LED
                self.pxs.set_random_pixel(colors=SimpleColors, wait=wait)
                self.pxs.show_pixels(brightness=0.2, wait=wait)

            # Reverse direction after hitting the right or left wall
            if x == self.res_x - tx or x == 0:
                # Reverse left/right direction
                dx = dx * -1

            # Reverse direction after hitting the ceiling or floor
            if y == (self.res_y - ty) or y == 0:
                # Reverse up/down direction
                dy = dy * -1

            time.sleep(wait)

    def show_name(self, name='John Doe'):
        self.clear()
        self.oled.text('Hello!', 5, 5)
        self.oled.text('My name is', 5, 15)
        self.oled.text(f'{name}', 5, 25)
        self.oled.show()

    def show_pronouns(self, pronouns):
        self.clear()
        self.oled.text(pronouns, 2, 15)
        self.oled.show()

    def show_rainbow(self):
        self.clear()
        self.oled.text('TASTE', 5, 5)
        self.oled.text('THE', 5, 15)
        self.oled.text('RAINBOW', 5, 25)
        self.oled.show()

    def show_selection(self):
        self.clear()
        self.oled.text('Please', 5, 5)
        self.oled.text('make a', 5, 15)
        self.oled.text('selection', 5, 25)
        self.oled.show()

    def show_startup(self):
        self.clear()
        self.oled.text('Pick a function', 5, 5)
        self.oled.text('using the ', 5, 15)
        self.oled.text('DIP switch', 5, 25)
        self.oled.show()

    def show_sws(self, wait=DEFAULT_WAIT):
        # Show a wicked cool intro
        self.clear()
        self.oled.text("It's time to", 5, 5)
        self.oled.text('sk3tch w/', 5, 15)
        self.oled.text('str3tch!', 5, 25)
        self.oled.show()
        time.sleep(wait)

    def show_sws_purge(self, wait=DEFAULT_WAIT):
        self.clear()
        self.oled.text('Purging old', 2, 5)
        self.oled.text('masterpieces', 2, 15)
        self.oled.text('...', 2, 25)
        self.oled.show()
        time.sleep(wait)

    def show_sws_purge_result(self, num=0, wait=DEFAULT_WAIT):
        self.clear()
        self.oled.text('Masterpieces', 2, 5)
        self.oled.text(f'purged: {num}', 2, 25)
        self.oled.show()
        time.sleep(wait)

    def show_sws_save(self, filename='', wait=DEFAULT_WAIT):
        self.clear()
        self.oled.text('Saving', 2, 5)
        self.oled.text('masterpiece:', 2, 15)
        self.oled.text(filename, 2, 25)
        self.oled.show()
        time.sleep(wait)

    def show_sws_save_error(self, text='', wait=DEFAULT_WAIT):
        self.clear()
        self.oled.text('Save error:', 5, 5)
        self.oled.text(text, 5, 15)
        self.oled.show()
        time.sleep(wait)


class PixelShow(object):
    # For the sake of this class, "pixel" refers to a multicolor LED
    def __init__(self, pixel_count=3, pin_num=16, brightness=DEFAULT_BRIGHTNESS):
        # Create the StateMachine with the ws2812 program, outputting on pin
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(pin_num))

        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)

        # Default brightness setting
        # TODO: make the brightness usage more consistent among functions
        self.brightness = brightness
        self.pixel_count = pixel_count

        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = array.array('I', [0 for _ in range(pixel_count)])

    def color_show(self, colors=['BLUE', 'GREEN', 'RED'], revolutions=3,
                   brightness=DEFAULT_BRIGHTNESS, wait=DEFAULT_WAIT):
        for r in range(revolutions):
            for i in range(self.pixel_count):
                self.set_pixel(i, color=random.choice(colors))
                self.show_pixels(brightness, wait=wait)

            time.sleep(wait)

    def clear(self):
        for i in range(self.pixel_count):
            self.set_pixel(i, color='BLACK')
        self.show_pixels(0)

    def color_chase(self, color, wait=DEFAULT_WAIT):
        self.clear()
        time.sleep(wait / 5)

        for i in range(self.pixel_count):
            self.set_pixel(i, color=color)
            self.show_pixels(self.brightness)
            time.sleep(wait)

    def get_random_colors(self, count=3):
        colors = []
        for i in range(count):
            colors.append(random.choice(list(Colors.keys())))
        return colors

    def hack(self, wait=DEFAULT_WAIT / 2):
        for i in range(self.pixel_count):
            if i % 2 == 0:
                self.set_pixel(i, color='ORANGE')
            else:
                self.set_pixel(i, color='PURPLE')
        self.show_pixels(self.brightness)
        time.sleep(wait)

        for i in range(self.pixel_count):
            if i % 2 == 0:
                self.set_pixel(i, color='BLACK')
            else:
                self.set_pixel(i, color='PURPLE')
        self.show_pixels(self.brightness)
        time.sleep(wait)

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.set_pixel(i, color=color)

    def pronoun(self, pronoun='NONE', wait=DEFAULT_WAIT):
        color = PronounColors.get(pronoun.upper(), DEFAULT_COLOR)
        self.color_chase(color)
        time.sleep(wait)

    def rainbow(self, wait=0.005):
        for j in range(255):
            for i in range(self.pixel_count):
                rc_index = (i * 256 // self.pixel_count) + j
                self.set_pixel(i, rgb=self.wheel(rc_index & 255), wait=wait)

            self.show_pixels(self.brightness)
            time.sleep(wait)

    def set_all_pixels(self, color, wait=DEFAULT_WAIT / 10):
        for i in range(self.pixel_count):
            self.set_pixel(i, color=color, wait=wait)
            time.sleep(wait)

    def set_pixel(self, i, color=DEFAULT_COLOR, rgb=None,
                  wait=DEFAULT_WAIT / 10):
        if rgb is None:
            rgb = Colors.get(color.upper(), Colors[DEFAULT_COLOR])

        self.ar[i] = (rgb[1] << 16) + (rgb[0] << 8) + rgb[2]
        time.sleep(wait)

    def set_random_pixel(self, pixel=None, color=None, colors=None,
                         wait=DEFAULT_WAIT):
        # Support various ways of setting a random color
        if color is None:
            if colors is None:
                color = random.choice(list(Colors.keys()))
            else:
                color = random.choice(colors)

        # Choose a random pixel
        if pixel is None:
            pixel = random.randint(0, self.pixel_count - 1)

        self.set_pixel(pixel, color=color, wait=wait)


    def show_pixels(self, brightness=DEFAULT_BRIGHTNESS, wait=DEFAULT_WAIT / 10):
        dimmer_ar = array.array('I', [0 for _ in range(self.pixel_count)])

        for i, c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * brightness)
            g = int(((c >> 16) & 0xFF) * brightness)
            b = int((c & 0xFF) * brightness)
            dimmer_ar[i] = (g << 16) + (r << 8) + b

        self.sm.put(dimmer_ar, 8)
        time.sleep(wait)

    def stoplight(self, wait=DEFAULT_WAIT):
        self.set_pixel(0, color='GREEN')
        self.show_pixels(self.brightness)
        time.sleep(wait * 2)

        self.set_pixel(0, color='BLACK')
        self.set_pixel(0, color='YELLOW')
        self.show_pixels(self.brightness)
        time.sleep(wait * 3)

        self.set_pixel(0, color='BLACK')
        self.set_pixel(0, color='RED')
        self.show_pixels(self.brightness)
        time.sleep(wait * 4)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colors are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return 0, 0, 0

        if pos < 85:
            return 255 - pos * 3, pos * 3, 0

        if pos < 170:
            pos -= 85
            return 0, 255 - pos * 3, pos * 3

        pos -= 170

        return pos * 3, 0, 255 - pos * 3
