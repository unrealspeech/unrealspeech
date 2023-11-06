import requests


class UnrealSpeechAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.v6.unrealspeech.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def stream(self, text, voice_id, bitrate="192k", speed=0, pitch=1.0, codec="libmp3lame", temperature=0.25):
        url = f"{self.base_url}/stream"
        payload = {
            "Text": text,
            "VoiceId": voice_id,
            "Bitrate": bitrate,
            "Speed": speed,
            "Pitch": pitch,
            "Codec": codec,
            "Temperature": temperature,
        }

        response = self._make_post_request(url, payload)
        return response.content

    def create_synthesis_task(self, text, voice_id, bitrate="192k", timestamp_type="word"):
        url = f"{self.base_url}/synthesisTasks"
        payload = {
            "Text": [text],
            "VoiceId": voice_id,
            "Bitrate": bitrate,
            "TimestampType": timestamp_type,
        }

        response = self._make_post_request(url, payload)
        response.raise_for_status()
        task_id = response.json()["SynthesisTask"]["TaskId"]
        return task_id

    def get_synthesis_task_status(self, task_id):
        url = f"{self.base_url}/synthesisTasks/{task_id}"
        while True:
            response = self._make_get_request(url)
            task_status = response.json()["SynthesisTask"]
            if task_status.get('TaskStatus') == 'completed':
                print(task_status)
                break
            else:
                print("Audiobook generation is in progress.")

    def speech(self, text, voiceId="Scarlett", bitrate="320k", timestamp_type="sentence"):
        url = f"{self.base_url}/speech"
        payload = {
            "Text": text,
            "VoiceId": voiceId,
            "Bitrate": bitrate,
            "OutputFormat": "uri",
            "TimestampType": timestamp_type
        }

        response = self._make_post_request(url, payload)
        return response.json()

    def _make_post_request(self, url, data):
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response

    def _make_get_request(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response
