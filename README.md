# Project Title

sk3tch w/ str3tch

## Description

This project was created for The Diana Initiative 2025 DIY badge and leverages the picozero, LEDs, RGB LEDs, OLED, and 4-bit dip switch.  This adds drawing functionality using only dip switches to create and save ascii art as well as provide other display options, such as displaying your Defcon handle, pronouns, and more.  This also attempts to make the original code from the badge project more readable with more organization of code.

## Getting Started

Build your TDI DIY 2025 badge (see Acknowledgement section for link to assembly video).  The picozero will automatically run main.py upon being turned on.

### Dependencies

* picozero.py (included in flashed picozero from TDI Maker Villiage, but also included here if needed)
* ssd1306.py (included in flashed picozero from TDI Maker Villiage, but also included here if needed)
* mpremote (for transfering files to/from picozero via CLI in python environment)

### Installing

* Download main.py and the TDI2025 directory
* Connect the picozero device to a computer via USB
* Use mpremote or Thonny to manage files on the picozero devices
* Copy main.py and the TDI2025 directory to the picozero (the included deploy.sh script can automate this)

### Executing program

* Deploy code
``` ./deploy.sh

## DIP Usage
# Main management of sk3tch
--- 1111: main sk3tch "lobby"
--- 0110: save sk3tch masterpiece to file on picozero as ascii art
--- 0000: reset sk3tch and the rest of the badge state

# sk3tch commands
--- 1110: turn/draw right
--- 0111: turn/draw left
--- 1100: turn/draw up
--- 0011: turn/draw down

# Other funzies
--- 1000: Display "He/Him/His"
--- 0100: Display "She/Her/Hers"
--- 0010: Display "They/Them/Theirs"
--- 0001: Display bouncing Defcon handle
--- 1010: Display real name
--- 1011: Display company name
--- 0110: Other
--- 0101: Other
--- 1101: Other

## Help
* main.py has variables you can modify to customize the messages displayed on the OLED.
* The dip switches can be tricky at times, not truly having switches enabled.  Resetting the switch usually helps.
* The picozero has very limited memory.  If you encounter a memory error, turning the badge on and off again can help.
* The bouncy animations take a little longer to finish.  There will be a noticeable delay between DIP actions.

## Authors

Contributors names and contact info

* [@str3tch](https://www.linkedin.com/in/jeromy-leugers-a747b96/)
* [The Diana Initiative](https://www.dianainitiative.org/)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [TDI Maker Villiage](https://sites.google.com/dianainitiative.org/makersvillage/home)
* [TDI 2025 DIY badge build video](https://www.youtube.com/watch?v=jirdqZoKM7A)
* [DomPizzie README template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
