import os
import pyaudio
import wave
from faster_whisper import WhisperModel

def record_chunk(p, stream, file_path, chunk_length=1):
    frames = []
    for _ in range(0, int(44100/1024*chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()


def main():
    model_size = "large-v2"
    model = WhisperModel(model_size, device='cpu', compute_type='auto')

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=44100, input=True, frames_per_buffer=1024)

    accumulated_transcription = ""

    try:
        while True:
            chunk_file = 'temp_chunk.wav'
            record_chunk(p, stream, chunk_file)
            segments, _ = model.transcribe(chunk_file)
            transcribed_text = " ".join(segment.text for segment in segments)
            print(transcribed_text)
            os.remove(chunk_file)

            accumulated_transcription += transcribed_text + " "

    except KeyboardInterrupt:
        print('stopping..')
        with open('log.txt', 'w') as log_file:
            log_file.write(accumulated_transcription)
    finally:
        print('LOG:' + accumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    main()
