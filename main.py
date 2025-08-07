# Author: str3tch @ Vegas 2.0 | dc702 / @JustJeromy
# Description: Dip Switch Etch a sk3tch...because crayons melt in Vegas.
# Other Credits: Some of the base code came from
#                The Diana Initiative Maker Village (thanks, Chris & Liam)
import framebuf
import time
import utime

time.sleep(0.1) # Wait for USB to become ready

# local imports
from TDI2025 import outputs
from TDI2025.inputs import DipSwitch
from TDI2025.sketch import Sketch


# Set daylight exists from 7am until 7pm (24HR format)
DAYLIGHT_START = 700
DAYLIGHT_END = 1900
DAYTIME_BRIGHTNESS = 0.1
EVENING_BRIGHTNESS = 0.5

# Minimum number of active pixels required to save masterpieces
SWS_MIN_ACTIVE_PIXELS = 32


# picozero has no real time, but kept to support other Pi devices
def is_daytime():
    hour = time.localtime()[3]
    if DAYLIGHT_START <= hour <= DAYLIGHT_END:
        return True
    else:
        return False


def main():
    dps = DipSwitch(4)
    lds = outputs.LedShow(pins=[14, 15])
    pxs = outputs.PixelShow(pixel_count=3, pin_num=16, brightness=0.1)
    ols = outputs.OledShow(res_x=128, res_y=32, scl_pin=27, sda_pin=26,
                           lds=lds, pxs=pxs)

    # Have SWS actions start at lower left corner of the screen
    # Adjusting step values will increase drawing speed by drawing n pixels
    # Minimum step of 1 enforced (1 step = 1 OLED pixel)
    sws = Sketch(res_x=128, res_y=32, start_x=1, start_y=32, step_x=2, step_y=1,
                 save_with_frame=True, pad_len=6)

    sws_cmds = {15: 'MAIN',
                14: 'RIGHT',
                7: 'LEFT',
                3: 'UP',
                12: 'DOWN',
                9: 'SAVE'}

    # Fresh start
    for color in pxs.get_random_colors(5):
        pxs.clear()
        ols.clear()
        pxs.color_chase(color, wait=0.1)
        ols.oled.text(color, 5, 5)
        ols.oled.scroll(5, 0)
        ols.oled.show()

    lds.pulse(count=5)
    ols.show_startup()

    last_cmd = -1
    while True:
        cmd = dps.get_value()

        # Adjust pixel brightness based on time of day
        # TODO: add a light sensor
        if is_daytime():
            pxs.brightness = DAYTIME_BRIGHTNESS
        else:
            pxs.brightness = EVENING_BRIGHTNESS

        # Reset
        if cmd == 0:
            if cmd == last_cmd:
                ols.show_startup()
                lds.pulse(wait=0)

            if last_cmd != cmd and last_cmd != -1:
                pxs.color_chase(color='dark red')
                ols.show_moving_text('reset', wait=0)
                sws.clear()
                lds.pulse(wait=0)
                pxs.clear()
                ols.clear()

            pxs.color_chase(color='dark green')

        if cmd == 1:
            if cmd != last_cmd:
                pxs.hack()
                ols.clear()
            ols.show_moving_text('str3tch', wait=0)

        if cmd == 2:
            pxs.clear()
            if cmd != last_cmd:
                ols.show_pronouns('They/Them/Theirs')
            pxs.pronoun('they')

        # 3: Reserved for SWS

        if cmd == 4:
            pxs.clear()
            if cmd != last_cmd:
                ols.show_pronouns('She/Her/Hers')
            pxs.pronoun('she')

        if cmd == 5:
            pxs.clear()
            if cmd != last_cmd:
                ols.show_rainbow()
            pxs.rainbow(wait=0)

        if cmd == 6:
            pxs.set_all_pixels('white', wait=0)
            ols.show_moving_ball(wait=0)

        # 7: Reserved for SWS

        if cmd == 8:
            pxs.clear()
            if cmd != last_cmd:
                ols.show_pronouns('He/Him/His')
            pxs.pronoun('he')

        # 9: Reserved for SWS

        if cmd == 10:
            if cmd != last_cmd:
                ols.show_name('Jeromy')
            pxs.stoplight()

        if cmd == 11:
            if cmd != last_cmd:
                ols.show_company('Packet House Security')
            pxs.color_show(wait=0.1)

        # 12: Reserved for SWS

        if cmd == 13:
            if cmd != last_cmd:
                ols.clear()
                ols.oled.text('Thonny is your', 5, 5)
                ols.oled.text('friendly IDE', 5, 15)
                ols.oled.text('for MicroPython', 5, 25)
                ols.oled.show()

                for color in pxs.get_random_colors(3):
                    pxs.color_chase(color, wait=0.2)

        # 14: Reserved for SWS

        # It's sk3tch w/ str3tch time!
        if cmd in sws_cmds:
            cmd_txt = sws_cmds.get(cmd, 'MAIN')

            if cmd_txt == 'MAIN':
                lds.pulse(count=5)
                pxs.set_all_pixels('blue', wait=0)
                pxs.show_pixels(brightness=0.1, wait=0)

                if cmd != last_cmd and last_cmd not in sws_cmds or sws_cmds[last_cmd] == 'SAVE':
                    # Show current masterpiece
                    if sws.get_active_pixel_count() >= 1:
                        ols.draw_pixels(sws.pixels)
                    else:
                        # Kick off SWS
                        ols.show_sws()
                        time.sleep(3)

            if cmd_txt == 'SAVE':
                lds.clear()
                lds.set_on(wait=0.5)
                pxs.set_all_pixels('blue')
                pxs.show_pixels(brightness=0.1)

                # Don't save duplicates
                if cmd == last_cmd:
                    ols.show_moving_text('SAVED', wait=0)
                    continue

                # Don't save tiny pieces of art
                if sws.get_active_pixel_count() < SWS_MIN_ACTIVE_PIXELS:
                    pxs.set_all_pixels('red')
                    pxs.show_pixels(brightness=0.1, wait=0)
                    lds.pulse(num=5)
                    ols.show_sws_save_error('too small', wait=3)
                    continue

                # Perform action
                masterpiece = f'sws_{str(int(time.time()))}.txt'
                ols.show_sws_save(masterpiece, wait=3)
                result = sws.save_to_file(masterpiece)
                if 'error' in result:
                    ols.show_sws_save_error(result, wait=3)

                # Run purger to ensure we don't run out of diskspace
                lds.clear()
                lds.set_on(wait=0.5)
                pxs.set_all_pixels('yellow')
                pxs.show_pixels(brightness=0.1, wait=0)
                ols.show_sws_purge(wait=3)
                purged_files = sws.purge_files(keep=10)

                # Give all clear feedback
                lds.clear()
                pxs.set_all_pixels('green')
                pxs.show_pixels(brightness=0.1, wait=0)
                ols.show_sws_purge_result(len(purged_files), wait=3)

            if cmd_txt == 'UP':
                # Feedback via LEDs
                lds.clear()
                lds.pulse(count=5, wait=0)

                # Feedback via pixels (RGB LEDs)
                pxs.set_all_pixels('yellow', wait=0)
                pxs.show_pixels(brightness=0.1, wait=0.01)

                # Perform action
                sws.move_up()
                ols.draw_pixels(sws.pixels, clear=False)

            if cmd_txt == 'DOWN':
                # Feedback via LEDs
                lds.clear()
                lds.pulse(count=5, wait=0)

                # Feedback via pixels (RGB LEDs)
                pxs.set_all_pixels('purple', wait=0)
                pxs.show_pixels(brightness=0.1, wait=0.01)

                # Perform action
                sws.move_down()
                ols.draw_pixels(sws.pixels, clear=False)

            if cmd_txt == 'LEFT':
                # Feedback via LEDs
                lds.clear()
                lds.pulse(count=5, wait=0)

                # Feedback via pixels (RGB LEDs)
                pxs.set_all_pixels('green', wait=0)
                pxs.show_pixels(brightness=0.1, wait=0)

                # Perform action
                sws.move_left()
                ols.draw_pixels(sws.pixels, clear=False)

            if cmd_txt == 'RIGHT':
                # Feedback via LEDs
                lds.clear()
                lds.pulse(count=5, wait=0)

                # Feedback via pixels (RGB LEDs)
                pxs.set_all_pixels('brown', wait=0)
                pxs.show_pixels(brightness=0.1, wait=0)

                # Perform action
                sws.move_right()
                ols.draw_pixels(sws.pixels, clear=False)

        last_cmd = cmd


if __name__ == '__main__':
    main()
