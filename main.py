from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可する場合
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可する場合
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可する場合
)

# リクエストデータのモデルを定義
class SantaRequest(BaseModel):
    message: str

# 日本語版GPT-2モデルのパイプラインを作成
generator = pipeline('text-generation', model='rinna/japanese-gpt2-medium', max_length=50)

@app.post("/")
def talk_to_santa(request: SantaRequest):
    # ユーザーからのメッセージに基づいてレスポンスを生成
    santa_prompt = f"サンタさんは {request.message} についてどう思いますか？"
    response = generator(santa_prompt, max_length=50)
    
    # 生成されたテキストから質問文を取り除く
    generated_text = response[0]['generated_text']
    try:
        # 質問文の終わりを見つける
        end_of_question = generated_text.index("についてどう思いますか？") + len("についてどう思いますか？")
        # 質問文以降のテキストを抽出
        answer = generated_text[end_of_question:].strip()
    except ValueError:
        # 質問文が見つからない場合は、全テキストをそのまま使用
        answer = generated_text
        
    return {"response": answer}