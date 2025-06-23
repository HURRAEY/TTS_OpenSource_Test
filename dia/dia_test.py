# dia_local_test.py
from dia.model import Dia
import os, soundfile as sf

os.environ["HF_TOKEN"] = "***REMOVED***"    # 읽기 권한 토큰

model = Dia.from_pretrained(
    "nari-labs/Dia-1.6B",
    device="mps",             # Mac-GPU 사용
    compute_dtype="float16"
)

text = "[S1] Dia is running on my Mac mini! [S2] Great!"
print("⏳ 모델 로딩 및 생성 중… (처음은 몇 분 걸릴 수 있어요)")
audio = model.generate(
    text,
    use_torch_compile=False,  # MPS는 compile 미지원
    verbose=True
)

model.save_audio("dia_output.mp3", audio)
print("✅ dia_output.mp3 저장 완료")

# 재생 가능한 형태로 변환 (선택사항)
try:
    data, samplerate = sf.read("dia_output.mp3")
    sf.write("dia_output.wav", data, samplerate)
    print("WAV 파일로도 변환되었습니다: dia_output.wav")
except Exception as e:
    print(f"WAV 변환 실패: {e}")

# JP 및 EN 대본 정의
jp_text = """[S1] 回転寿司食べに行きます？ [S2] 良いですね。 [S1] ソン室長、クルーズの準備しなさい。 [S3] はい。 [S2] 回転寿司食べるのになんでクルーズなんですか？ [S1] ５大洋を一周しながら食べるお寿司が回転寿司じゃないの。 [S2] 皿が回るんじゃなくて船が回るんだ。 [S1] ソン室長、始めのコースはブラックタイガーのえび寿司で予約しなさい。 [S3] オサチュルド大西洋店で予約いたします。 [S2] オサチュルドが大西洋まで進出した？ [S1] サメの握り、召し上がったことは？ [S2] いいえ。 [S1] でしたら、次のコースはチョウザメの握りでお願いするわ。 [S3] ウネンゴル太平洋店で、予約いたします。 [S1] レシートレビューを書けば、キャビア巻きくださるところよね？ [S3] 左様で御座います。 [S2] 太平洋でもレシートレビューを書くんだなぁ。 [S1] あなた、お刺身はお好き？ [S2] はい！ [S1] でしたら次は、深海魚の刺身丼にいたしましょう。 [S3] タムナ水産市場インド店で、予約いたします。 [S2] 深海魚でも刺身するんだな。 [S1] デザートは何かしら？ [S3] 北極海にまいりますと、骨付き鶏モモの揚げパンがございます。南極海では練乳たっぷりのカキ氷をお召し上がりいただけます。 [S1] ソンシムダン北極海店に行くか、ソルビン南極海店に行くか、悩みますわね。 [S2] でもこれ、全部実在するんですか？ [S1] わたくし専用の一人用フードショップですわ。 [S2] こんなに食べたら高くないですか？ [S1] 平日ランチなら、お一人様19,900ドルしかしないわ。 [S2] ウォンじゃなくてドル... [S1] ええ。 [S2] ランチ一食が、僕の年収分かぁ… [S1] こういうところに住んでいるんですね。 [S2] はい。 [S1] でも、シンクとベッドが同じ空間にあるのはなぜですか？ [S2] え？ [S1] ああ！これは家政婦さんたちの休憩室ですね。 [S2] 休憩室ではありませんが。 [S1] では？ [S2] ワンルームです。 [S1] ワンルーム。なるほど。１番目のルームは見せてもらったわ。２番目のルームを見せて。 [S2] これが全部ですが？ [S1] これが家の全部ですって？ [S2] はい。 [S1] ではプールはどこ？ [S2] プールはありませんが。 [S1] 家にプールがないんですって？ [S2] ええ。 [S1] 面白いわ。 [S1] ねえ、でもテレビつけっぱなし？ [S2] うちにはテレビがありませんが。 [S1] 人の声が聞こえるけど。 [S2] ああ、上の階の騒音です。 [S1] ああ、これが階間騒音なのね。面白いわ。 [S2] あ、はい。 [S1] えっと、これは何？ [S2] 君と食べようと思って粉食を用意したんだ。 [S1] 私、粉食知ってるわ。 [S2] どうやって知ってるの？ [S1] 叔父が選挙の時期になると、市場でいつも食べるのよ。 [S2] そうなんだ。 [S1] あっ、そうだ。 [S1] これ。 [S2] これは何？ [S1] 新居祝いのプレゼントよ。 [S2] 大丈夫だよ、君。 [S1] 快適に乗り回してね。 [S2] そうじゃなくて…家に駐車場がないんだ。 [S1] 駐車場がないって？ [S1] 面白いわ."""

en_text = """[S1] Shall we go eat conveyor-belt sushi? [S2] Sounds good. [S1] Mr. Song, get the cruise ready. [S3] Yes. [S2] Why a cruise if we're just eating conveyor-belt sushi? [S1] Conveyor-belt sushi means eating sushi while circling the five oceans, doesn't it? [S2] So it's not the plates that rotate, but the ship. [S1] Mr. Song, book the first course: black-tiger prawn sushi. [S3] I'll reserve it at the Osachuldo Atlantic branch. [S2] Osachuldo expanded all the way to the Atlantic? [S1] Have you ever tried shark sushi? [S2] No. [S1] Then let's make the next course sturgeon sushi. [S3] I'll book it at the Unengo Pacific branch. [S1] That's the place that gives you a caviar roll if you write a receipt review, right? [S3] Exactly. [S2] They even ask for receipt reviews out in the Pacific, huh. [S1] Do you like sashimi? [S2] Yes! [S1] Then next let's have a deep-sea fish sashimi rice bowl. [S3] I'll reserve it at the Tamna Fish-Market Indian-Ocean branch. [S2] They even serve deep-sea fish as sashimi. [S1] What about dessert? [S3] In the Arctic Ocean there's fried bread stuffed with chicken drumsticks; in the Antarctic Ocean you can enjoy shaved ice with lots of condensed milk. [S1] I'm torn between Seongsimdang's Arctic branch and Sulbing's Antarctic branch. [S2] Do all of these places actually exist? [S1] They're one-person food shops exclusively for me. [S2] Wouldn't it be expensive to eat all this? [S1] A weekday lunch is only $19,900 per person. [S2] Not won, but dollars… [S1] Yes. [S2] One lunch equals my annual salary… [S1] So, this is home for you. [S2] Yes. [S1] But why are the sink and bed in the same space? [S2] What? [S1] Aha! This must be the staff's break room. [S2] It's not a break room. [S1] Then what is it? [S2] It's a studio. [S1] A studio. Got it. I've seen the first room. Show me the second. [S2] This is all of it. [S1] This is the whole house? [S2] Yes. [S1] Then, where's the pool? [S2] There's no pool. [S1] No pool in the house? [S2] No. [S1] What a laugh. [S1] By the way, is the TV on? [S2] I don't have a TV. [S1] But I hear voices. [S2] Oh, that's noise from the upstairs neighbor. [S1] Oh, this is that upstairs noise. What a laugh. [S2] Okay. [S1] Oh, what's this? [S2] I prepared some Korean snacks for us. [S1] I know Korean snacks. [S2] How do you know? [S1] My uncle always eats them at the market during elections. [S2] Oh, I see. [S1] Oh, right. [S1] This. [S2] What's this? [S1] A house-warming gift. [S2] It's okay, honey. [S1] Drive around comfortably. [S2] Well… There's no parking space here. [S1] No parking space? [S1] What a laugh."""

scripts = {
    "jp": jp_text,
    "en": en_text,
}

print("⏳ 모델 로딩 및 생성 중… (처음은 몇 분 걸릴 수 있어요)")

for lang, script in scripts.items():
    print(f"⏳ {lang} 음성 생성 중…")
    audio = model.generate(
        script,
        use_torch_compile=False,  # MPS는 compile 미지원
        verbose=True
    )

    mp3_file = f"dia_output_{lang}.mp3"
    wav_file = f"dia_output_{lang}.wav"

    model.save_audio(mp3_file, audio)
    print(f"✅ {mp3_file} 저장 완료")

    try:
        data, samplerate = sf.read(mp3_file)
        sf.write(wav_file, data, samplerate)
        print(f"WAV 파일로도 변환되었습니다: {wav_file}")
    except Exception as e:
        print(f"WAV 변환 실패 ({lang}): {e}")