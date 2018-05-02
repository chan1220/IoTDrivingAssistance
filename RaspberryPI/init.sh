sudo rfcomm release all
sudo rfcomm bind 0 00:1D:A5:00:37:85

rdate -s time.bora.net

python3 /home/pi/develop/main.py
