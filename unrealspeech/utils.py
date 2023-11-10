from playsound import playsound
import requests
import shutil
import subprocess
from typing import Iterator
import importlib
from pydub import AudioSegment
import simpleaudio as sa
import requests
import io


def is_installed(lib_name: str) -> bool:
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    return True


def is_string(value):
    return isinstance(value, str)


def play(audio: bytes, notebook: bool = False, use_ffmpeg: bool = True) -> None:
    if isinstance(audio, bytes):
        if notebook:
            from IPython.display import Audio, display

            display(Audio(audio, rate=44100, autoplay=True))
        elif use_ffmpeg:
            if not is_installed("ffplay"):
                message = (
                    "ffplay from ffmpeg not found, necessary to play audio. "
                    "On mac you can install it with 'brew install ffmpeg'. "
                    "On linux and windows you can install it from https://ffmpeg.org/"
                )
                raise ValueError(message)
            args = ["ffplay", "-autoexit", "-", "-nodisp"]
            proc = subprocess.Popen(
                args=args,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = proc.communicate(input=audio)
            proc.poll()

        else:
            try:
                import io

                import sounddevice as sd
                import soundfile as sf
            except ModuleNotFoundError:
                message = (
                    "`pip install sounddevice soundfile` required when `use_ffmpeg=False` "
                )
                raise ValueError(message)
            sd.play(*sf.read(io.BytesIO(audio)))
            sd.wait()
    elif isinstance(audio, object):
        play_stream_audio(audio)


def save(audio: bytes, filename: str) -> None:
    if isinstance(audio, bytes):
        with open(filename, "wb") as f:
            f.write(audio)
    elif isinstance(audio, object):
        download_audio(audio, filename)


def download_audio(audio_data, filename):
    """
    This function takes a dictionary that should contain an 'OutputUri' key.
    It attempts to download the audio from the URI and save it to a file.

    :param audio_data: Dictionary with 'OutputUri' key
    :return: None
    """
    output_uri = audio_data.get('OutputUri')

    if output_uri:
        try:
            audio_url = output_uri

            if isinstance(output_uri, list):
                audio_url = output_uri[0]

            response = requests.get(audio_url)
            response.raise_for_status()

            # Save the audio to a file
            with open(filename, "wb") as audio_file:
                audio_file.write(response.content)
            print("Audio downloaded and saved successfully.")
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

    else:
        raise Exception("No 'OutputUri' key found in the audio data.")


def play_audio_from_url(audio_url, duration=None):
    required_packages = ["pydub", "simpleaudio"]

    missing_packages = [
        pkg for pkg in required_packages if importlib.util.find_spec(pkg) is None]
    if missing_packages:
        raise ModuleNotFoundError(
            f"Required packages not found: {', '.join(missing_packages)}")

    try:
        # Download audio from the URL
        response = requests.get(audio_url)
        response.raise_for_status()

        # Convert the audio to a format that simpleaudio can play
        audio_data = AudioSegment.from_file(io.BytesIO(response.content))

        # Play the audio for the specified duration or the entire audio if duration is None
        play_obj = sa.play_buffer(audio_data.raw_data, num_channels=audio_data.channels,
                                  bytes_per_sample=audio_data.frame_width, sample_rate=audio_data.frame_rate)

        if duration is not None:
            # Wait for the specified duration
            sa.wait(int(duration * 1000))  # Convert seconds to milliseconds
        else:
            # Wait for the audio to finish playing
            play_obj.wait_done()

    except Exception as e:
        print(f"An error occurred: {e}")


def play_stream_audio(audio_data):
    output_uri = audio_data.get('OutputUri')
    try:
        if output_uri:
            audio_url = output_uri

            if isinstance(output_uri, list):
                audio_url = output_uri[0]

            try:
                play_audio_from_url(audio_url)
                print("Playing audio.")
            except requests.exceptions.HTTPError as http_err:
                raise Exception(f"HTTP error occurred: {http_err}")
            except Exception as err:
                raise Exception(f"An error occurred: {err}")

        else:
            raise Exception("No 'OutputUri' key found in the audio data.")

    except Exception as e:
        raise Exception(
            f"An error occurred while trying to play the audio: {e}")
