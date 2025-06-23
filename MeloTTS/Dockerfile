FROM python:3.9-slim
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e .
RUN pip install --upgrade "boto3>=1.36.0" "botocore>=1.36.0"
RUN python -m unidic download
RUN python - <<'PY'
import nltk, shutil, os, pathlib
nltk.download('averaged_perceptron_tagger', quiet=True)
root = nltk.data.find('taggers/averaged_perceptron_tagger')
dst = pathlib.Path(root).parent / 'averaged_perceptron_tagger_eng'
dst.mkdir(parents=True, exist_ok=True)
for f in os.listdir(root):
    shutil.copy(os.path.join(root, f), dst)
PY
RUN python melo/init_downloads.py

CMD ["python", "./melo/app.py", "--host", "0.0.0.0", "--port", "8888"]