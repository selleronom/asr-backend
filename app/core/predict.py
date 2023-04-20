import torch
import torchaudio
from transformers import AutoModelForCTC, AutoProcessor


class SpeechRecognition:
    def __init__(self):
        print("init SpeechRecognition")

    def load_model(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(
            "KBLab/wav2vec2-large-voxrex-swedish")
        self.model = AutoModelForCTC.from_pretrained(
            "KBLab/wav2vec2-large-voxrex-swedish").to(self.device)

        return self

    def predict(self, batch):
        features = self.processor(
            batch["speech"], sampling_rate=16_000, return_tensors="pt", padding=True)

        input_values = features.input_values.to(self.device)
        attention_mask = features.attention_mask.to(self.device)

        with torch.no_grad():
            logits = self.model(
                input_values, attention_mask=attention_mask).logits

        pred_ids = torch.argmax(logits, dim=-1)

        batch["predicted"] = self.processor.batch_decode(pred_ids)[0]
        return batch

    def predict_audio_file(self, data):
        features = self.processor(
            data["speech"], sampling_rate=data["sampling_rate"], padding=True, return_tensors="pt")
        input_values = features.input_values.to(self.device)
        attention_mask = features.attention_mask.to(self.device)
        with torch.no_grad():
            logits = self.model(
                input_values, attention_mask=attention_mask).logits
            decoded_results = []
            for logit in logits:
                pred_ids = torch.argmax(logit, dim=-1)
                mask = pred_ids.ge(1).unsqueeze(-1).expand(logit.size())
                vocab_size = logit.size()[-1]
                voice_prob = torch.nn.functional.softmax(
                    (torch.masked_select(logit, mask).view(-1, vocab_size)), dim=-1)
                comb_pred_ids = torch.argmax(voice_prob, dim=-1)
                decoded_results.append(self.processor.decode(comb_pred_ids))

        return decoded_results

    def load_speech_with_file(self, audio_file):
        batch = {}
        speech, _ = torchaudio.load(audio_file)
        batch["speech"] = speech.squeeze(0).numpy()
        batch["sampling_rate"] = 16_000
        return batch
