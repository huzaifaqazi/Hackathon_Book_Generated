# Chapter 4.2: Whisper for Voice Command Extraction

A fundamental component of any Vision-Language-Action (VLA) system that interacts with humans via spoken commands is a robust Speech-to-Text (ASR) engine. **OpenAI Whisper** has emerged as a state-of-the-art, open-source ASR model that can accurately transcribe spoken language into text. Its excellent performance, multilingual capabilities, and availability make it an ideal choice for extracting voice commands for humanoid robots.

This chapter will introduce you to Whisper, explain how it works, and guide you through its integration into a VLA pipeline for your humanoid robot.

## 1. What is OpenAI Whisper?

Whisper is a pre-trained neural network for Automatic Speech Recognition (ASR). Trained on a massive dataset of diverse audio and text, it exhibits remarkable performance in transcribing speech in many languages and even translating those languages into English.

### Key Features and Advantages for Robotics:

-   **High Accuracy**: Whisper's large training dataset and robust architecture lead to highly accurate transcriptions, even in challenging acoustic environments.
-   **Robustness**: It is capable of handling various accents, background noise, and different speaking styles.
-   **Multilingual Support**: Can transcribe in numerous languages and translate from those languages into English, which is valuable for global robotics applications.
-   **Open Source**: Freely available for use, modification, and deployment.
-   **Model Sizes**: Available in various sizes (tiny, base, small, medium, large), allowing for a trade-off between accuracy and computational cost. Smaller models are suitable for edge devices like NVIDIA Jetson (refer to Chapter 0.3).

## 2. How Whisper Works (High-Level)

Whisper is an encoder-decoder Transformer model.

-   **Encoder**: Takes raw audio input and converts it into a sequence of abstract representations (features).
-   **Decoder**: Takes these features and generates a sequence of text tokens, effectively transcribing the speech.

The model is trained end-to-end on paired audio and text data, learning to directly map sound waves to written words.

## 3. Integrating Whisper into a ROS 2 VLA System

The most straightforward way to integrate Whisper into a ROS 2 VLA system is by creating a ROS 2 Python node that leverages the `openai-whisper` Python package. This node will listen for audio input, process it with Whisper, and publish the transcribed text to a ROS 2 topic.

### 3.1. Installation

First, ensure you have the `openai-whisper` Python package installed in your ROS 2 environment (preferably within a Python virtual environment). You also need `ffmpeg` for audio processing.

```bash
# Install ffmpeg (if not already installed)
sudo apt update && sudo apt install -y ffmpeg

# Activate your Python virtual environment (if used)
source ~/physical_ai_robotics_venv/bin/activate

# Install openai-whisper
pip install -U openai-whisper
```

### 3.2. Audio Input for Whisper

Whisper requires audio data, typically as `.wav` files or byte streams. For a robot, this audio would come from a microphone.

-   **Physical Robot**: Connect a USB microphone to your Jetson or workstation. Use `pyaudio` or a ROS 2 audio driver package to capture audio data and publish it to a ROS 2 topic (e.g., `audio_common` package from ROS 1, or custom implementation for ROS 2).
-   **Simulation**: In Isaac Sim, you might simulate a microphone by feeding pre-recorded audio files into your Whisper node, or you might need a dedicated simulation plugin if one becomes available.

### 3.3. Creating a ROS 2 Whisper Node

Let's outline the structure of a `whisper_asr_node.py` within your ROS 2 package (e.g., `humanoid_vla_pkg`).

```python
# whisper_asr_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # For publishing transcribed text
# from audio_common_msgs.msg import AudioData # Example for audio input if using audio_common
import numpy as np
import whisper
import pyaudio # For direct microphone access (example, for real robot)
import wave # For saving audio (debugging)
import threading # For non-blocking audio capture

class WhisperASRNode(Node):
    def __init__(self):
        super().__init__('whisper_asr_node')
        self.declare_parameter('whisper_model_name', 'small')
        self.whisper_model_name = self.get_parameter('whisper_model_name').value
        self.get_logger().info(f'Loading Whisper model: {self.whisper_model_name}')

        try:
            self.model = whisper.load_model(self.whisper_model_name)
            self.get_logger().info('Whisper model loaded successfully.')
        except Exception as e:
            self.get_logger().error(f'Failed to load Whisper model: {e}')
            rclpy.shutdown()
            return

        self.text_publisher = self.create_publisher(String, '/humanoid/voice_command', 10)

        # --- For direct microphone input (on physical robot) ---
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000, # Whisper expects 16kHz
                                      input=True,
                                      frames_per_buffer=1024)
        self.frames = []
        self.recording_duration = 5 # seconds of audio to capture at a time
        self.record_interval = 1 # process every 1 second
        self.recording_timer = self.create_timer(self.record_interval, self.record_and_transcribe_callback)
        self.get_logger().info("Whisper ASR Node initialized. Listening for voice commands...")

        # --- For ROS 2 audio topic input (alternative) ---
        # self.audio_subscription = self.create_subscription(
        #     AudioData,
        #     '/audio/raw', # ROS 2 topic for raw audio data
        #     self.audio_callback,
        #     10
        # )
        # self.audio_buffer = []

    def record_and_transcribe_callback(self):
        # Read audio from microphone
        data = self.stream.read(16000 * self.record_interval, exception_on_overflow=False)
        self.frames.append(data)

        # Only process if we have enough audio for 'recording_duration'
        if len(self.frames) * self.record_interval >= self.recording_duration:
            # Concatenate audio frames and convert to numpy array
            audio_data = b''.join(self.frames)
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            # Reset frames buffer
            self.frames = []

            # Transcribe in a separate thread to not block ROS 2 spinning
            threading.Thread(target=self._transcribe_audio, args=(audio_np,)).start()

    def _transcribe_audio(self, audio_np):
        self.get_logger().info("Transcribing audio...")
        try:
            # The transcribe function expects a numpy array of audio samples
            # Ensure audio_np is mono and 16kHz, which pyaudio is configured for
            result = self.model.transcribe(audio_np, language='en') # Specify language for better performance
            transcribed_text = result["text"]
            self.get_logger().info(f'Transcribed: "{transcribed_text}"')

            # Publish the transcribed text
            msg = String()
            msg.data = transcribed_text
            self.text_publisher.publish(msg)

        except Exception as e:
            self.get_logger().error(f'Error during transcription: {e}')

    def destroy_node(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    whisper_asr_node = WhisperASRNode()
    rclpy.spin(whisper_asr_node)
    whisper_asr_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

-   **`whisper.load_model(self.whisper_model_name)`**: Loads the specified Whisper model. `small` or `medium` are good starting points for Jetson.
-   **`pyaudio`**: Used here for direct microphone access. For a more robust ROS 2 solution, you'd integrate with a ROS 2 package that handles audio capture and publishing to a topic.
-   **`self.text_publisher`**: Publishes the transcribed text as a `std_msgs/msg/String` to `/humanoid/voice_command`. This topic will be consumed by the LLM cognitive planner.
-   **`threading.Thread`**: Crucial! Transcribing with Whisper can take a few seconds, especially with larger models. Running it in a separate thread prevents your ROS 2 node from blocking the main `rclpy.spin()` loop.

## 4. Considerations for Deployment on Jetson

-   **Model Size**: Choose a Whisper model size that balances accuracy with the computational resources available on your Jetson device. `small` or `base` models are often suitable for real-time inference on Orin.
-   **Hardware Acceleration**: Ensure that `whisper` is able to leverage the GPU for inference. Depending on your Python environment, you might need to install `torch` with CUDA support.
-   **Audio Pipeline**: Design a robust audio capture pipeline from the robot's microphone to the Whisper node.
-   **Noise Robustness**: Optimize microphone placement and consider audio pre-processing techniques to minimize background noise, which can impact ASR accuracy.

## Conclusion

OpenAI Whisper provides an excellent, accessible solution for extracting voice commands in VLA systems for humanoid robots. By integrating a ROS 2 node that captures audio, transcribes it with Whisper, and publishes the resulting text, you establish the crucial linguistic input channel for your robot. This transcribed text can then be fed into a cognitive planning module, enabling your humanoid to understand and respond to human instructions.
