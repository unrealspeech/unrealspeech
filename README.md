# Unreal Speech API Python Package

Unreal Speech API Python package allows you to easily integrate the Unreal Speech API into your Python applications for text-to-speech (TTS) synthesis. This package provides convenient methods for working with the Unreal Speech API, including generating speech, managing synthesis tasks, and streaming audio.

## Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Obtaining an API Key](#obtaining-an-api-key)
- [Usage](#usage)
  - [Initializing the UnrealSpeechAPI](#initializing-the-unrealspeechapi)
  - [Generating Speech](#generating-speech)
  - [Managing Synthesis Tasks](#managing-synthesis-tasks)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Installation

You can install the Unreal Speech API Python package using pip:

```bash
pip install unrealspeech-api
```

## Available endpoints

| Endpoint                 | Description                                  |
| ------------------------ | -------------------------------------------- |
| `/stream`                | Stream audio for short, time-sensitive cases |
| `/speech`                | Generate speech with options (MP3 format)    |
| `/synthesisTasks`        | Manage synthesis tasks for longer text       |
| `/synthesisTasks/TaskId` | Check the status of a synthesis task         |

## Common Request Body Schema

| Property | Type   | Required? | Default Value | Allowed Values                             |
| -------- | ------ | --------- | ------------- | ------------------------------------------ |
| VoiceId  | string | Required  | N/A           | Scarlett, Liv, Dan, Will, Amy              |
| Bitrate  | string | Optional  | 192k          | 16k, 32k, 48k, 64k, 128k, 192k, 256k, 320k |
| Speed    | float  | Optional  | 0             | -1.0 to 1.0                                |
| Pitch    | float  | Optional  | 1.0           | 0.5 to 1.5                                 |

## Parameter Details

- **VoiceId:**

  - Dan: Young Male
  - Will: Mature Male
  - Scarlett: Young Female
  - Liv: Young Female
  - Amy: Mature Female

- **Bitrate:** Defaults to 192k. Use lower values for low bandwidth or to reduce the transferred file size. Use higher values for higher fidelity.

- **Speed:** Defaults to 0. Examples:

  - 0.5: makes the audio 50% faster. (i.e., 60-second audio becomes 42 seconds)
  - -0.5: makes the audio 50% slower. (i.e., 60-second audio becomes 90 seconds.)

- **Pitch:** Defaults to 1. However, on the landing page, we default male voices to 0.92 as people tend to prefer lower/deeper male voices.

## Rate Limit

| Plan  | Requests per second |
| ----- | ------------------- |
| Free  | 1                   |
| Basic | 2                   |
| Pro   | 8                   |

## Obtaining an API Key

To use the Unreal Speech API, you'll need to obtain an API key by signing up for an account on the Unreal Speech website. Once you have an API key, you can use it to initialize the UnrealSpeechAPI class.

## Usage

#### Initializing the UnrealSpeechAPI

First, import the UnrealSpeechAPI class:

```python
from unrealspeech.api import UnrealSpeechAPI
```

Then, initialize the API with your API key:

```python
api_key = 'YOUR_API_KEY'
speech_api = UnrealSpeechAPI(api_key)
```

## Generating Speech

You can generate speech by providing a text string and optional parameters:

```python
text_to_speech = "This is a sample text."
timestamp_type = "sentence"  # Choose from 'sentence' or 'word'
voice_id = "Scarlett"  # Choose the desired voice
audio_data = speech_api.speech(text_to_speech, timestamp_type, voice_id)

# Save the audio to a file
with open("output.mp3", "wb") as audio_file:
    audio_file.write(audio_data)

```

## Streaming Audio

For short and time-sensitive cases, you can use the /stream endpoint to stream audio:

```python
# Stream audio
text_to_stream = "This is a short text to be synthesized."
audio_data = speech_api.stream(text_to_stream, voice_id, bitrate="192k", speed=0, pitch=1.0, codec="libmp3lame", temperature=0.25)

```

## Managing Synthesis Tasks

You can manage synthesis tasks for longer text using the `/synthesisTasks` endpoint:

```python
# Create a synthesis task
task_id = speech_api.create_synthesis_task(text_to_speech, voice_id, bitrate="320k", timestamp_type="word")

# Check the task status
task_status = speech_api.get_synthesis_task_status(task_id)

```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
