# ブログ記事管理

アフィリエイトブログ用の記事管理アプリ。スマホ・PC 両方から、アイデア出し → 本文生成 → 修正 → 承認 までを行う。
（恋愛チャンネルの台本管理システムと同じ構成：静的HTML + GitHub保存 + ブラウザからClaude API）

## 機能
- `＋新規テーマ` … テーマ・アイデアを入力（1テーマ1記事＝1投稿）
- `💡アイデア&生成` … テーマ/アイデア/キーワードから本文を自動生成
- `✏️編集` … 本文を直接編集 ＋「修正指示」でClaudeに直してもらう
- `👁プレビュー` … 記事の見た目を確認
- ステータス：💡アイデア → ✍️作成中 → ✅承認済 → 📤投稿済
- `✅承認済`タブは並び替え可（PC=ドラッグ / スマホ=↑↓）。並び順は `posts/_order.json` に保存

## 構成
- `index.html` — メインUI
- `posts/post_xxx.json` — 記事データ（1ファイル1記事）
- `posts/_order.json` — 承認済みの投稿順
- `posts/schema.json` — データ形式

## 投稿フロー
1. アプリで記事を `✅承認済` にして、投稿したい順に並べる
2. PC の Claude Code に「上から投稿して」と指示
3. Claude Code が `_order.json` の順に WordPress の**下書き**へ作成し、各記事を `📤投稿済` に更新

## セットアップ
1. このフォルダを GitHub の新規リポジトリ `blog-posts` に push
2. リポジトリの Settings → Pages で `main` ブランチを公開 → 表示されたURLにアクセス
3. `index.html` 先頭の `REPO` がリポジトリ名（`ユーザー名/blog-posts`）と一致しているか確認
4. アプリ右上の ⚙️ で以下を入力（端末ごとに1回）
   - Anthropic API Key（本文生成用）
   - GitHub Token（保存用 / Contents 書き込み権限）
   - 生成モデル（既定 `claude-sonnet-4-6`）

## メモ
- API Key・Token はブラウザの localStorage に保存（端末内のみ）。WordPress のパスワードはアプリに保存しない（投稿はPC側のClaude Codeが担当）。
