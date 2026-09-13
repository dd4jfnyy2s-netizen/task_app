# ログイン機能付きタスク管理Webアプリ

## 概要

FlaskとSQLiteを使用して作成したタスク管理Webアプリです。

ユーザー登録・ログイン機能を実装し、ログインしたユーザーごとに
自分のタスクを管理できるようにしています。

## 主な機能

- ユーザー登録
- ログイン・ログアウト
- パスワードのハッシュ化
- タスクの追加
- タスクの編集
- タスクの削除
- タスクの完了・未完了の切り替え
- ユーザーごとのタスク管理
- 未ログインユーザーのアクセス制限
- 入力チェック

## 使用技術

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2

## データベース

### usersテーブル

- id
- name
- password

### tasksテーブル

- id
- user_id
- title
- completed

## アプリの構成

```text
task_app/
├── app.py
├── database.py
├── task.db
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── register.html
    ├── login.html
    ├── tasks.html
    └── edit.html