
# ver.9(完成版)

## atcoderの提出コードをそのまま用いることはできるようになった

### app.pyでの変更点
ver.8
```
 global_context = {'sys': sys, 'input': io.StringIO(input_data).read}
```
ver.9
```
stdin = io.StringIO(input_data)
global_context = {'sys': sys, 'input': stdin.readline}
```

---

# ver.8

## atcoderの提出コードをそのまま用いることはできないが、テキスト読み込みのコードに書き換えることで、実行時間の測定ができる

### 本アプリでのスタイル
```
lines = input().strip().splitlines()
N = int(lines[0])
P = list(map(int,lines[1].split()))
A=0
for i in range(N):
  flag=0
  for j in range(i):
    if P[i]>P[j]:
      flag=1
      break
  if flag==0:
    A+=1
print(A)
```

### AtCoderでのスタイル
```
N = int(input())
P = list(map(int,input().split()))
A=0
for i in range(N):
  flag=0
  for j in range(i):
    if P[i]>P[j]:
      flag=1
      break
  if flag==0:
    A+=1
print(A)
```
----

% python app.py

http://127.0.0.1:5000
