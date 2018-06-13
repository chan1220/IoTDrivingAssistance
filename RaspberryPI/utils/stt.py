
from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue


# [END import_libraries]

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/MyMic-b737a86ac104.json'

class MicrophoneStream(object):
	"""Opens a recording stream as a generator yielding the audio chunks."""
	def __init__(self, rate, chunk):
		self._rate = rate
		self._chunk = chunk

		# Create a thread-safe buffer of audio data
		self._buff = queue.Queue()
		self.closed = True

	def __enter__(self):
		self._audio_interface = pyaudio.PyAudio()
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paInt16,
			# The API currently only supports 1-channel (mono) audio
			# https://goo.gl/z757pE
			channels=1, rate=self._rate,
			input=True, frames_per_buffer=self._chunk,
			# Run the audio stream asynchronously to fill the buffer object.
			# This is necessary so that the input device's buffer doesn't
			# overflow while the calling thread makes network requests, etc.
			stream_callback=self._fill_buffer,
		)

		self.closed = False
		# print('녹음 시작!')

		return self

	def __exit__(self, type, value, traceback):
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		# print('녹음 종료해버리기')
		# Signal the generator to terminate so that the client's
		# streaming_recognize method will not block the process termination.
		self._buff.put(None)
		self._audio_interface.terminate()

	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		"""Continuously collect data from the audio stream, into the buffer."""
		self._buff.put(in_data)
		return None, pyaudio.paContinue

	def generator(self):
		while not self.closed:
			# Use a blocking get() to ensure there's at least one chunk of
			# data, and stop iteration if the chunk is None, indicating the
			# end of the audio stream.
			chunk = self._buff.get()
			if chunk is None:
				# print('녹음 완료?')
				return
			data = [chunk]

			# Now consume whatever other data's still buffered.
			while True:
				try:
					chunk = self._buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break

			yield b''.join(data)
# [END audio_stream]


def listen_print_loop(responses, callback):

	num_chars_printed = 0
	for response in responses:
		if not response.results:
			continue

		result = response.results[0]
		if not result.alternatives:
			continue

		transcript = result.alternatives[0].transcript

		overwrite_chars = ' ' * (num_chars_printed - len(transcript))

		if not result.is_final:
			# sys.stdout.write(transcript + overwrite_chars + '\r')
			# sys.stdout.flush()
			# print(transcript)
			callback(transcript)
			num_chars_printed = len(transcript)
		
		else:
			return transcript

class STT():
	def __init__(self):
		language_code = 'ko-KR'
		self.client = speech.SpeechClient()
		config = types.RecognitionConfig(
			encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
			sample_rate_hertz=RATE,
			language_code=language_code)
		self.streaming_config = types.StreamingRecognitionConfig(
			config=config,
			interim_results=True)

	def get_str(self, callback):
		with MicrophoneStream(RATE, CHUNK) as stream:
			audio_generator = stream.generator()
			requests = (types.StreamingRecognizeRequest(audio_content=content)
						for content in audio_generator)

			responses = self.client.streaming_recognize(self.streaming_config, requests)

			# Now, put the transcription responses to use.
			return listen_print_loop(responses, callback)

if __name__ == '__main__':
	stt = STT()
	while True:
		print('문장 : ',stt.get_str())
