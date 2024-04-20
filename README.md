# tz_flask


---

FlaskはPythonのウェブアプリケーションフレームワークであり、アプリケーションの構造は一般的に以下のような基本的な構成を持ちます:

アプリケーションフォルダー構造: Flaskアプリケーションは通常、特定のフォルダ構造内に配置されます。一般的な構造は以下の通りです:

```
your_project/
├── app/
│   ├── static/        # CSS、JavaScript、画像などの静的ファイル
│   ├── templates/     # Jinja2テンプレートファイル
│   ├── __init__.py    # アプリケーションの初期化
│   ├── routes.py      # アプリケーションのエンドポイント (ルート) 定義
├── venv/              # 仮想環境
├── config.py          # アプリケーションの設定
├── requirements.txt   # 依存関係のリスト
├── run.py             # アプリケーションを実行するためのスクリプト
```

init.py: このファイルはFlaskアプリケーションのエントリーポイントです。ここでアプリケーションを作成し、設定を読み込み、拡張機能を初期化します。
routes.py: これはFlaskアプリケーションのエンドポイント (ルート) を定義するファイルです。各URLに対してどのような処理を行うかを記述します。
staticフォルダ: CSS、JavaScript、画像などの静的ファイルを格納するためのフォルダです。ブラウザから直接アクセスできます。
templatesフォルダ: Jinja2テンプレートを格納するためのフォルダです。これらのテンプレートを使用して動的なコンテンツを生成します。
config.py: アプリケーションの設定を格納するファイルです。データベースの接続情報やシークレットキーなどの構成情報を含めることができます。
requirements.txt: アプリケーションの依存関係を含むファイルです。pip install -r requirements.txt を使用して依存関係をインストールします。
run.py: アプリケーションを実行するためのスクリプトです。通常、このファイルはFlaskアプリケーションを起動するためのエントリーポイントとして使用されます。


---
pip install flask

app.pyを作成

templatesディレクトリを作成し,中にindex.htmlを作成

python app.py

http: //127.0.0.1:5000/にアクセス

