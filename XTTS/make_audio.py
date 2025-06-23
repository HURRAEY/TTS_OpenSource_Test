import re, unicodedata
from pathlib import Path
import soundfile as sf
import numpy as np
from collections import defaultdict
from TTS.api import TTS

def is_japanese(text):
    for ch in text:
        name = unicodedata.name(ch, '')
        if 'CJK UNIFIED' in name or 'HIRAGANA' in name or 'KATAKANA' in name:
            return True
    return False

script = [
"So, this is home for you.",
"Yes.",
"But, why are the sink and bed in the same space?",
"What?", 
"Aha! This must be the staff's break room.",
"It's not a break room.",
"Then what is it?",
"It's a studio.",
"A studio.",
"Got it. I've seen the first room. Show me the second one.",
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
"Oh, that's just upstairs noise.",
"Oh, this is that upstairs noise.",
"What a laugh.",
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
"Well, the thing is…",
"There's no parking space here.",
"No parking space?",
"What a laugh.",
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
"ランチ一食が、僕の年収分かぁ…"
]

out_dir = Path("generated")
out_dir.mkdir(exist_ok=True)

print("모델 로드 중… (처음이면 1GB 다운로드)")
model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

sr = None
pieces = []

lang_dirs = {"ko": "korean", "ja": "japanese", "en": "english"}
# 언어별 파편 저장소
pieces_per_lang: dict[str, list[np.ndarray]] = defaultdict(list)
counters = defaultdict(int)

def get_lang(text: str) -> str:
    if is_japanese(text):
        return "ja"
    # 아주 단순: 한글 포함하면 ko, 아니면 en
    if any("HANGUL" in unicodedata.name(ch, "") for ch in text):
        return "ko"
    return "en"

speaker_map = {"ko": "speakers/male.wav", "ja": "speakers/female.wav", "en": "speakers/calm_female.wav"}

for text in script:
    lang = get_lang(text)
    counters[lang] += 1
    idx = counters[lang]

    sub_dir = out_dir / lang_dirs[lang]
    sub_dir.mkdir(parents=True, exist_ok=True)
    wav_path = sub_dir / f"line_{idx:03}.wav"

    print(f"[{lang} #{idx:03}] {text[:30]}…")
    model.tts_to_file(text=text, language=lang, speaker_wav=speaker_map[lang], file_path=str(wav_path))

    wav, sr = sf.read(wav_path)
    pieces_per_lang[lang].append(wav)

# 언어별 합본 작성
for lang, chunks in pieces_per_lang.items():
    merged = np.concatenate(chunks)
    sub_dir = out_dir / lang_dirs[lang]
    full_path = sub_dir / "output_full.wav"
    sf.write(full_path, merged, sr)
    print(f"{lang} 합본 저장 → {full_path}")
