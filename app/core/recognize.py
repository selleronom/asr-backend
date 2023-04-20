import io

from pydub import AudioSegment
from pydub.silence import split_on_silence
from spylls.hunspell import Dictionary

from app.core.predict import SpeechRecognition

sp = SpeechRecognition()

sp.load_model()


class AudioProcessing:
    def __init__(self):
        print("init AudioProcessing")

    def recognition(self, file):
        contents = file.file.read()
        print("audio_file", file.filename)

        sound = AudioSegment.from_file(io.BytesIO(contents))
        audio_chunks = split_on_silence(
            sound, min_silence_len=500, silence_thresh=-40)

        result = []
        # result = str

        for i, chunk in enumerate(audio_chunks):
            output_file = "/tmp/chunk{0}.wav".format(i)
            print("Exporting file", output_file)
            chunk.export(output_file, format="wav", parameters=[
                "-acodec",  "pcm_s16le",  "-ac",  "1",  "-ar", "16000"])
            speech = sp.load_speech_with_file(output_file)

            result.append(sp.predict_audio_file(speech))
            # print(type(sp.predict_audio_file(speech)))
            # result += str(sp.predict_audio_file(speech))
            # x = ",".join(str(v) for v in result)

        flattened = [val for sublist in result for val in sublist]
        x = ", ".join(flattened)
        # print(type(x))
        return x
