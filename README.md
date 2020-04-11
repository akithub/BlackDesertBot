# BlackDesertBot

BlackDesert 用の bot

# 目次

- [BlackDesertBot](#blackdesertbot)
- [目次](#%e7%9b%ae%e6%ac%a1)
- [環境](#%e7%92%b0%e5%a2%83)
- [導入](#%e5%b0%8e%e5%85%a5)
- [実行](#%e5%ae%9f%e8%a1%8c)
- [機能](#%e6%a9%9f%e8%83%bd)
  - [通知系](#%e9%80%9a%e7%9f%a5%e7%b3%bb)
    - [VC チャンネル入退室通知](#vc-%e3%83%81%e3%83%a3%e3%83%b3%e3%83%8d%e3%83%ab%e5%85%a5%e9%80%80%e5%ae%a4%e9%80%9a%e7%9f%a5)
  - [コマンド系](#%e3%82%b3%e3%83%9e%e3%83%b3%e3%83%89%e7%b3%bb)
    - [kujira](#kujira)
    - [Note](#note)

# 環境

python3

# 導入

1. discord の導入
   ```
   $python3 -m pip install -U discord.py
   ```
2. config file の作成
   ```
   $cp config_tp.ini config.ini
   ```
3. config の中身を記述する

GUILD_ID を記入する。
ID は該当のサーバを右クリックし、メニュー -> ID をコピー でクリップボードにコピーできる。

```ini
[General]
token=    # Botのトークン
guild_id= # サーバのID (int)
```

# 実行

```
$python3 DCbot.py
```

# 機能

## 通知系

### VC チャンネル入退室通知

config.ini にて以下を指定する。
ID は該当のチャンネルを右クリックし、メニュー -> ID をコピー でクリップボードにコピーできる。

```ini
[Voice inout]
output_channel_id= # 通知を書き出すテキストチャンネルのID (int)
voice_channel_id=  # 入退室を検知するボイスチャンネルのID (int)
```

## コマンド系

### kujira

```
+kujira
```

クジラが出現しているチャンネルを調査する際に用いる。
コマンドを入力すると、以下のように発言する

```
捜索完了CH：
        Ba
        Se
        Me
        Va
        Mg
        ka
=============================
未捜索CH
Ba
Se
Me
Ba
Mg
Ka
```

未捜索 CH の下に並ぶメッセージのリアクションをクリックすることで、該当のリアクションが捜索完了 CH に追加される。
調査済みのチャンネルに該当する数字リアクションをクリックして追加することで、以下のようにコメントに追加される。

### Note

メモを追加する。

- 登録
  ```
  +note add "メモタイトル" "内容"
  ```
  or
  ```
  +note a "メモタイトル" "内容"
  ```
  同じタイトルのメモは追加できない。
  メモを置き換える場合は `+note replace` を使う
- タグ付きで登録
  ```
  +note add "メモタイトル" "内容" "タグ1,タグ2"
  ```
- 閲覧
  ```
  +n メモタイトル
  ```
  以下のように、登録されたメモの内容を BOT が返す
  ```
  内容
  ```
- 全て閲覧
  ```
  +note all
  ```
  以下のように、登録されたメモを BOT が返す
  ```
  タイトル: 内容(tag:['タグ 1', 'タグ 2'])
  ```
- タグで検索
  "タグ" がついているものだけを検索して BOT が返す
  ```
  +note tag "タグ"
  ```
  or
  ```
  +note t "タグ"
  ```
- メモの置き換え
  ```
  +note replace "タイトル" "内容" "タグ"
  ```
- メモの消去
  ```
  +note delete "タイトル"
  ```
  or
  ```
  +note del "タイトル"
  ```
