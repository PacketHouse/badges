#!/bin/bash
echo "Copying files to pi..."
mpremote cp TDI2025/inputs.py :TDI2025/inputs.py
mpremote cp TDI2025/outputs.py :TDI2025/outputs.py
mpremote cp TDI2025/sketch.py :TDI2025/sketch.py
mpremote cp TDI2025/sws_logo.csv :TDI2025/sws_logo.csv
mpremote cp main.py :main.py
