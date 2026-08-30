# WebScraper

Pythonで実装した書籍情報のWebスクレイピングデモです。

[Books to Scrape](https://books.toscrape.com/) から書籍情報を取得し、データを検証・整形したうえでCSVファイルとして出力します。

## 概要

以下の書籍情報を取得します。

- 書籍タイトル
- 価格
- 在庫状況
- 評価
- 商品URL

複数ページにわたる書籍情報を取得できるよう、ページネーションにも対応しています。

## 使用技術

- Python 3.14
- Requests
- Beautiful Soup
- pandas
- pytest

## 主な機能

### Webスクレイピング

`requests` と `Beautiful Soup` を使用して書籍情報を取得します。

### ページネーション

「Next」リンクを辿り、複数ページの書籍情報を取得します。

### データクレンジング

取得した価格・在庫・評価などを適切なデータ型へ変換します。

### データバリデーション

以下の項目をチェックします。

- タイトルの欠損
- 価格の欠損・不正値
- 評価の欠損・範囲外
- 在庫情報の型
- URLの欠損

### エラーハンドリング

HTTP通信時のエラーを捕捉し、ログへ記録します。

また、`Retry` を使用して一時的なHTTPエラーに対するリトライにも対応しています。

### CSV出力

取得・検証したデータをpandas DataFrameへ変換し、CSVとして保存します。

## テスト

pytestを使用して、以下の処理をテストしています。

- 価格変換
- 在庫情報変換
- 評価変換
- スクレイピング処理
- ページネーション
- HTTPエラー処理
- データバリデーション
- DataFrame生成
- CSV出力

テスト実行：

```bash
pytest
```

## 実行方法

### 1. リポジトリを取得

```bash
git clone https://github.com/JunKjpn/WebScraper.git
cd WebScraper
```

### 2. 仮想環境を作成

```bash
python -m venv .venv
```

### 3. 仮想環境を有効化

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

### 4. パッケージをインストール

```bash
pip install -r requirements.txt
```

### 5. 実行

```bash
python -m webscraper.scraper
```

実行すると `output/` にCSVファイルが生成されます。

## 出力例

```csv
title,price,availability,rating,url
A Light in the Attic,51.77,True,3,https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
Tipping the Velvet,53.74,True,1,https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html
Soumission,50.1,True,1,https://books.toscrape.com/catalogue/soumission_998/index.html
```

## ディレクトリ構成

```text
WebScraper/
├── webscraper/
│   ├── __init__.py
│   └── scraper.py
├── tests/
│   └── test_scraper.py
├── output/
├── requirements.txt
└── README.md
```

## ポートフォリオとしてのポイント

- PythonによるWebスクレイピング
- Beautiful SoupによるHTML解析
- requestsによるHTTP通信
- ページネーション処理
- HTTPエラーハンドリング
- リトライ処理
- データクレンジング・バリデーション
- pandasによるデータ加工
- CSV出力
- pytestによる単体テスト
- `unittest.mock` による外部通信のモックテスト

## 注意事項

本プロジェクトはスクレイピング学習・技術デモを目的としています。

実際のWebサイトをスクレイピングする際は、対象サイトの利用規約・robots.txt・アクセス制限等を確認し、サーバーへ過度な負荷をかけないよう適切な間隔を設けてアクセスしてください。

## データ提供元

本デモではスクレイピング練習用サイトである [Books to Scrape](https://books.toscrape.com/) を利用しています。
