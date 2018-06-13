import json
import urllib.request
import subprocess

class TTS():
	def play_mp3(self, path):
		subprocess.Popen(['mpg123', '-q', path]).wait()

	def play_tts(self, text, speaker='mijin'):
		client_id = "6vNW1jYKk6ETlhsx4QAB"           # <= 변경 
		client_secret = "80mPSyDfbA" # <= 변경
		encText = urllib.parse.quote(text)
		data = "speaker=" + speaker + "&speed=0&text=" + encText; # jinho,mijin, clara, matt, shinji, yuri
		url = "https://openapi.naver.com/v1/voice/tts.bin"
		request = urllib.request.Request(url)
		request.add_header("X-Naver-Client-Id",client_id)
		request.add_header("X-Naver-Client-Secret",client_secret)
		response = urllib.request.urlopen(request, data=data.encode('utf-8'))
		rescode = response.getcode()

		if(rescode==200):
		    print("TTS mp3 저장")
		    response_body = response.read()
		    with open("temp", "wb") as f:
		        f.write(response_body)
		    self.play_mp3('temp')
		else:
		    print("Error Code:" + rescode)
