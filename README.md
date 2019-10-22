# SetsugekkaBot

雪月花用のbot

# 目次

- [SetsugekkaBot](#setsugekkabot)
- [目次](#%e7%9b%ae%e6%ac%a1)
- [環境](#%e7%92%b0%e5%a2%83)
- [導入](#%e5%b0%8e%e5%85%a5)
- [実行](#%e5%ae%9f%e8%a1%8c)
- [機能](#%e6%a9%9f%e8%83%bd)
  - [通知系](#%e9%80%9a%e7%9f%a5%e7%b3%bb)
    - [VCチャンネル入退室通知](#vc%e3%83%81%e3%83%a3%e3%83%b3%e3%83%8d%e3%83%ab%e5%85%a5%e9%80%80%e5%ae%a4%e9%80%9a%e7%9f%a5)
  - [コマンド系](#%e3%82%b3%e3%83%9e%e3%83%b3%e3%83%89%e7%b3%bb)
    - [kujira](#kujira)

# 環境

python3

# 導入

1. discordの導入
    ```
    $python3 -m pip install -U discord.py
    ```
2. config file の作成
    ```
    $cp config_tp.ini config.ini
    ```
3. config の中身を記述する

GUILD_ID を記入する。
IDは該当のサーバを右クリックし、メニュー -> IDをコピー でクリップボードにコピーできる。

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

### VCチャンネル入退室通知

config.iniにて以下を指定する。
IDは該当のチャンネルを右クリックし、メニュー -> IDをコピー でクリップボードにコピーできる。

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

未捜索CHの下に並ぶメッセージのリアクションをクリックすることで、該当のリアクションが捜索完了CHに追加される。
調査済みのチャンネルに該当する数字リアクションをクリックして追加することで、以下のようにコメントに追加される。
