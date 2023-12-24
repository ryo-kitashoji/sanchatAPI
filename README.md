# サンタ風chatAPI
rinnaのモデルにサンタ風のプロンプトを入力することでそれらしく振舞うようにしました．

## 環境構築
以下のコマンドを実行
```
git clone https://github.com/ryo-kitashoji/sanchatAPI.git
cd sanchatAPI/
python3 -m venv env # venv（pythonの仮想環境ツール）がない場合はpip install venvを実行
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app
# 外部公開する場合は uvicorn main:app --host=0.0.0.0
```

## 実行方法
```
curl -X POST http://localhost:8000/ -H "Content-Type: application/json" -d "{\"message\":\"プレゼントをください\"}"
```