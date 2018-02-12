# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
1. Google SDK 설치

# Create an environment variable for the correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk

위의 줄 복붙
https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu?hl=ko


2. pip3 install google-cloud-speech

"""


from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from threading import Thread
import time

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 1000)  # 1ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True
        self.isPause = False

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()


        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def pause(self):
        if self.isPause == False:
            self.isPause = True


    def resume(self):
        if self.isPause == True:
            self.isPause = False


    def status(self):
        return self.isPause

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        if self.isPause == False:
            self._buff.put(in_data)
        #else
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return

            data = [chunk]

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



class STT(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.language_code = 'ko-KR'  # a BCP-47 language tag

        self._buff = queue.Queue()

        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=self.language_code)
        self.streaming_config = types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)

        self.mic = None
        self.status = True

        self.daemon = True
        self.start()

    def __eixt__(self):
        self._buff.put(None)

    def run(self):
        with MicrophoneStream(RATE, CHUNK) as stream:
            self.mic = stream
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = self.client.streaming_recognize(self.streaming_config, requests)

            # Now, put the transcription responses to use.
            self.listen_print_loop(responses, stream)
        self._buff.put(None)
        self.status = False

    def pauseMic(self):
        if self.mic is not None:
            self.mic.pause()

    def resumeMic(self):
        if self.mic is not None:
            self.mic.resume()

    # 인식된 Text 가져가기
    def getText(self, block = True):
        return self._buff.get(block=block)

    # 음성인식 처리 루틴
    def listen_print_loop(self, responses, mic):
        num_chars_printed = 0
        try:
            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                overwrite_chars = ' ' * (num_chars_printed - len(transcript))
                if not result.is_final:
                    sys.stdout.write(transcript + overwrite_chars + '\r')
                    sys.stdout.flush()
                    #### 추가 ### 화면에 인식 되는 동안 표시되는 부분.
                    num_chars_printed = len(transcript)
                else:
                    # 큐에 넣는다.
                    self._buff.put(transcript+overwrite_chars)
                    num_chars_printed = 0
        except:
            return



def main():
    gsp = STT()
    while True:
        # 음성 인식 될때까지 대기 한다.
        stt = gsp.getText()
        # 만약 None이 반환되면
        if stt is None:
            break
        print(stt)
        time.sleep(0.01)
        # 꺼지라하면 꺼진다.
        if ('꺼져' in stt):
            break


if __name__ == '__main__':
    main()
