# Author: str3tch @ Vegas 2.0 | dc702 / @JustJeromy
# Description: A tool for drawing using dip switches and whatnot
import os
import time


class Sketch(object):
    def __init__(self, res_x=128, res_y=32, start_x=-1, start_y=-1,
                 step_x=1, step_y=1, wrap_screen=False, save_with_frame=False,
                 pad_len=6, signature='\\ sk3tch w/ str3tch /'):
        self.max_x = res_x
        self.max_y = res_y
        self.min_x = 1
        self.min_y = 1
        self.res = res_x * res_y
        self.pad_len = pad_len
        self.pixels = [0] * self.res
        self.save_with_frame = save_with_frame
        self.signature = signature

        # Reach a wall?  Teleport to the opposite wall.
        self.wrap_screen = wrap_screen

        # Number of pixels to skip when drawing
        self.step_x = step_x
        self.step_y = step_y

        # Set the initial position
        if 0 < start_x < self.max_x:
            self.x = start_x
        else:
            self.x = self.min_x

        if 0 < start_y < self.max_y:
            self.y = start_y
        else:
            self.y = self.max_y

        self.add_pixel(self.current_pixel())

    def __str__(self):
        return self.get_art()

    def add_frame(self, lines=[], background=' ', foreground='*', border='#',
                  pad_len=None, signature=None):
        # Returns ascii art with a frame and signature
        ###################################################
        #       ******   *       *       *    ******      #
        #      *          *     * *     *    *            #
        #       *****      *   *   *   *      *****       #
        #            *      * *     * *            *      #
        #      ******        *       *       ******       #
        ###################################################
        #                    signature                    #
        ###################################################
        if self.signature and signature is None:
            signature = self.signature
            
        if self.pad_len > 0 and pad_len is None:
            pad_len = self.pad_len

        frame_width = len(border) + pad_len + self.max_x + pad_len + len(border)

        # Build top and bottom frame border
        fb = border * frame_width

        # Build left prefix and right suffix
        l = f'{border}{background * pad_len}'
        r = f'{background * pad_len}{border}'

        # Truncate signatures that are too long
        max_signature_len = frame_width - (len(border) * 2)
        if len(signature) > max_signature_len:
            print(f'Signature truncated: {len(signature)}/{max_signature_len}')
            if max_signature_len > 0:
                signature = signature[0:max_signature_len]
            else:
                print(f'Signature removed due to invalid max length: {max_signature_len}')
                signature = ''

        # Amount of padding on each side (prefix and suffix)
        sig_pad_len = int((max_signature_len - len(signature)) / 2)
        sig_pad = background * sig_pad_len
        sp = f'{border}{sig_pad}'
        ss = f'{sig_pad}{border}'

        # Add additional padding to signature if length is odd
        if len(signature) % 2 == 1:
            ss = f' {ss}'

        # Build vertical padding
        vertical_pad = f'{border}{background * max_signature_len}{border}'
        vpl = [vertical_pad] * pad_len

        # Build signature line
        if signature:
            sl = f'{sp}{signature}{ss}'
        else:
            sl = ''

        # Prep top of framed masterpiece
        framed_lines = [fb]
        framed_lines.extend(vpl)

        # Add art to the frame
        for line in lines:
            framed_lines.append(f'{l}{line}{r}')

        # Add bottom of frame
        framed_lines.extend(vpl)
        framed_lines.append(fb)

        # Append signature to bottom of frame
        if sl:
            framed_lines.append(sl)
            framed_lines.append(fb)

        return '\n'.join(framed_lines)

    def add_pixel(self, position):
        # Adds a specified pixel
        position = int(position) - 1
        if position >= self.res or position < 0:
            print(f'Invalid position: {position}')
        else:
            self.pixels[position] = 1

    def clear(self):
        self.pixels = [0] * self.res
        self.x = self.min_x
        self.y = self.min_y
        self.add_pixel(self.current_pixel())

    def current_pixel(self):
        return ((self.y - 1) * self.max_x) + self.x

    def get_active_pixel_count(self):
        active = 0
        for i in range(self.res):
            if self.pixels[i] == 1:
                active += 1

        return active

    def get_art(self, background=' ', border='#', foreground='*',
                include_frame=False, pad_len=4, signature=None):
        if self.signature and signature is None:
            signature = self.signature

        lines = []
        line = ''
        for i in range(self.res):
            if len(line) == self.max_x:
                lines.append(line)
                line = ''

            if self.pixels[i]:
                line += foreground
            else:
                line += background

        # Ensure the last line is added
        if len(lines) < self.max_y:
            lines.append(line)

        if include_frame:
            # Add a frame to make-a the art look-a very
            art = self.add_frame(lines=lines, background=background,
                                 border=border, foreground=foreground,
                                 pad_len=pad_len, signature=signature)
        else:
            art = '\n'.join(lines)

        return art

    def move_left(self):
        # Make sure we always have a movement
        if self.step_x < 1:
            self.step_x = 1

        # Add a pixel for every step
        for i in range(self.step_x):
            self.x -= 1
            if self.x <= 0:
                if self.wrap_screen:
                    self.x = self.max_x
                else:
                    self.x = self.min_x
            self.add_pixel(self.current_pixel())

    def move_right(self):
        # Make sure we always have a movement
        if self.step_x < 1:
            self.step_x = 1

        # Add a pixel for every step
        for i in range(self.step_x):
            self.x += 1
            if self.x >= self.max_x:
                if self.wrap_screen:
                    self.x = self.min_x
                else:
                    self.x = self.max_x
            self.add_pixel(self.current_pixel())

    def move_up(self):
        # Make sure we always have a movement
        if self.step_y < 1:
            self.step_y = 1

        # Add a pixel for every step
        for i in range(self.step_y):
            self.y -= 1
            if self.y <= 0:
                if self.wrap_screen:
                    self.y = self.max_y
                else:
                    self.y = self.min_y
            self.add_pixel(self.current_pixel())

    def move_down(self):
        # Make sure we always have a movement
        if self.step_y < 1:
            self.step_y = 1

        # Add a pixel for every step
        for i in range(self.step_y):
            self.y += 1
            if self.y >= self.max_y:
                if self.wrap_screen:
                    self.y = self.min_y
                else:
                    self.y = self.max_y
            self.add_pixel(self.current_pixel())

    # Covert a number to  x, y
    def pixel_to_coord(self, num):
        y = int(num / self.max_x)
        x = (num % self.max_x)
        return x, y

    def purge_files(self, path='.', keep=8):
        sws_files = []

        for item in reversed(os.listdir(path)):
            if item.startswith('sws_') and item.endswith('.txt'):
                sws_files.append(item)

        print(f'{len(sws_files)} masterpieces found')
        purged_files = []
        if len(sws_files) > keep:
            # If our sort worked above, the most recent files should be up front
            purged_files = sws_files[keep:]
            for file in purged_files:
                print(f'Burning {file}...')
                os.remove(file)

        return purged_files

    def save_to_file(self, filename=None):
        try:
            if filename is None:
                filename = f'sws_{str(int(time.time()))}.txt'

            with open(filename, 'w') as file:
                file.write(f'{self.get_art(include_frame=self.save_with_frame)}\n')
        except MemoryError as error:
            print(f'Memory error: {error}')
            filename = 'memory error'

        return filename


def main():
    x = 32
    y = 16
    s = Sketch(x, y)
    while True:
        direction = input(': ').upper()
        if direction.startswith('L'):
            s.move_left()
        elif direction.startswith('R'):
            s.move_right()
        elif direction.startswith('D'):
            s.move_down()
        elif direction.startswith('U'):
            s.move_up()
        elif direction.startswith('Q'):
            break
        else:
            print(f'Invalid direction: {direction}')

    print(s.get_art(include_frame=True, signature='test'))


if __name__ == '__main__':
    main()
