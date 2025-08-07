# Author: str3tch @ Vegas 2.0 | dc702 / @JustJeromy
# Description: Handles the inputs (e.g. dip switch)
from picozero import Switch


class DipSwitch(object):
    def __init__(self, switch_count=4):
        self.switch_values = {}

        # Make the right most switch the lowest bit (e.g. 8421)
        bit = 1
        for num in reversed(range(switch_count)):
            self.switch_values[num] = Switch(bit)
            bit += 1

    def get_value(self):
        total = 0
        # Treat each switch as a bit in a binary number
        for switch_num in self.switch_values:
            if self.switch_values[switch_num].value == True:
                total += 2 ** switch_num

        return total
