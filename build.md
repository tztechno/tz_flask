
```

http://127.0.0.1:5000


type A:
元のHTMLコードをFlaskのテンプレートとして配置します。
Flaskで利用できるようにファイル名をindex.htmlとしてtemplatesフォルダに保存します。

type B:
app.pyでISSのデータを取得し、JSON形式で提供するエンドポイントを作成しました。
index.htmlでは、JavaScriptを使ってFlaskのエンドポイントからデータを取得し、地図に表示します。
Python（Flask）がデータの取得を担当し、JavaScriptがそのデータを使ってクライアントサイドで地図に表示する。


```