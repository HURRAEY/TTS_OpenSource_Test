import os
import argparse
import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


def load_model(model_id: str, device: str):
    """Load Parler-TTS model/tokenizer on the specified device."""
    model = ParlerTTSForConditionalGeneration.from_pretrained(model_id).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    return model, tokenizer


def generate_audio(lines, model, tokenizer, device, out_dir):
    """Generate a wav file for every sentence in *lines*."""
    os.makedirs(out_dir, exist_ok=True)

    for idx, text in enumerate(lines, 1):
        # Choose a basic description depending on language (ASCII ≈ English)
        if text.isascii():
            description = "A clear neutral English voice."
        else:
            description = "日本語の明瞭な声。"

        desc_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)

        with torch.no_grad():
            wav = model.generate(input_ids=desc_ids, prompt_input_ids=prompt_ids)

        audio = wav.cpu().numpy().squeeze()
        out_path = os.path.join(out_dir, f"line_{idx:02d}.wav")
        sf.write(out_path, audio, model.config.sampling_rate)
        print(f"[✓] Saved {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Parler-TTS audio clips for provided script lines.")
    parser.add_argument("--model_id", default="parler-tts/parler-tts-mini-v1", help="Model checkpoint ID")
    parser.add_argument("--device", default="cuda:0" if torch.cuda.is_available() else "cpu", help="Device")
    parser.add_argument("--out_dir", default="tts_outputs", help="Directory to save wav files")
    args = parser.parse_args()

    script_lines = [
        # Japanese lines
        "回転寿司食べに行きます？",
        "良いですね。",
        "ソン室長、クルーズの準備しなさい",
        "はい。",
        "回転寿司食べるのになんでクルーズなんですか？",
        "５大洋を一周しながら食べるお寿司が回転寿司じゃないの。",
        "皿が回るんじゃなくて船が回るんだ。",
        "ソン室長、始めのコースはブラックタイガーのえび寿司で予約しなさい。",
        "オサチュルド大西洋店で予約いたします。",
        "オサチュルドが大西洋まで進出した？",
        "サメの握り、召し上がったことは？",
        "いいえ。",
        "でしたら、次のコースはチョウザメの握りでお願いするわ。",
        "ウネンゴル太平洋店で、予約いたします。",
        "レシートレビューを書けば、キャビア巻きくださるところよね？",
        "左様で御座います。",
        "太平洋でもレシートレビューを書くんだなぁ。",
        "あなた、お刺身はお好き？",
        "はい！",
        "でしたら次は、深海魚の刺身丼にいたしましょう。",
        "タムナ水産市場インド店で、予約いたします。",
        "深海魚でも刺身するんだな。",
        "デザートは何かしら？",
        "北極海にまいりますと、骨付き鶏モモの揚げパンがございます。南極海では練乳たっぷりのカキ氷をお召し上がりいただけます。",
        "ソンシムダン北極海店に行くか、ソルビン南極海店に行くか、悩みますわね。",
        "でもこれ、全部実在するんですか？",
        "わたくし専用の一人用フードショップですわ",
        "こんなに食べたら高くないですか？",
        "平日ランチなら、お一人様19,900ドルしかしないわ。",
        "ウォンじゃなくてドル...",
        "ええ。",
        "ランチ一食が、僕の年収分かぁ…",
        # English lines
        "So, this is home for you.",
        "Yes.",
        "But, why are the sink and bed in the same space?",
        "What?",
        "Aha! This must be the staff's break room.",
        "It's not a break room.",
        "Then what is it?",
        "It's a studio.",
        "A studio. Got it. I've seen the first room. Show me the second one.",
        "This is all of it.",
        "This is the whole house?",
        "Yes.",
        "Then, where's the pool?",
        "There's no pool.",
        "No pool in the house?",
        "No.",
        "What a laugh.",
        "By the way, is the TV on?",
        "I don't have a TV.",
        "But I hear voices.",
        "Oh, that's noise from the upstairs neighbor.",
        "Oh, this is that upstairs noise. What a laugh.",
        "Okay.",
        "Oh, what's this, though?",
        "I prepared some Korean snacks for us.",
        "I know Korean snacks.",
        "How do you know?",
        "My uncle always eats them at the market during elections.",
        "Oh, I see.",
        "Oh, right.",
        "This.",
        "What's this?",
        "A housewarming gift.",
        "It's okay, honey.",
        "Drive around comfortably.",
        "Well, the thing is… There's no parking space here.",
        "No parking space?",
        "What a laugh.",
    ]

    device = args.device
    print(f"[i] Using device: {device}")
    model, tokenizer = load_model(args.model_id, device)
    generate_audio(script_lines, model, tokenizer, device, args.out_dir)


if __name__ == "__main__":
    main() 