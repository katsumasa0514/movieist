![](https://user-images.githubusercontent.com/72243833/115001680-d47fb680-9ede-11eb-8784-74e50fe05146.png)
 
 <h1 align="center">Movieist</h2>
 
 <p align="center">
  <a href="PWA公式サイトURL"><img src="https://user-images.githubusercontent.com/72243833/115094538-e30ab400-9f58-11eb-8513-01a1a84f9ca1.png" width="80px;" height="80px" /></a>
  <a href="PWA公式サイトURL"><img src="https://user-images.githubusercontent.com/72243833/115094546-e9009500-9f58-11eb-8dcc-83eb1ec8f8af.png" width="80px;" /></a>
  <a href="Firebase公式サイトURL"><img src="https://user-images.githubusercontent.com/72243833/115094547-e9992b80-9f58-11eb-8c10-15a6f0a679ab.png" width="80px;" /></a>
  <a href="firealpaca公式サイトURL"><img src="https://user-images.githubusercontent.com/72243833/115094550-eaca5880-9f58-11eb-9de4-def708c8c04b.png" width="80px;" /></a>
  <a href="sweetalert公式サイトURL"><img src="https://user-images.githubusercontent.com/72243833/115094552-ebfb8580-9f58-11eb-9a5e-1bc426b59066.png" width="80px;" /></a>
</p>
 
## アプリ内容
 
ユーザーが投稿した、映画のレビューから観たい映画を探すWEBアプリです。

映画情報サイトが数多くある中、ユーザー間の情報共有の部分のみ抜き出し作成しました。
ユーザーの投稿を、最新の投稿、ランキング順、ジャンル分けなどで表示して、感覚的に使っていただけるアプリになっています。

映画情報サイトで観たい映画を探す際に、既に観た映画や、有名どころの映画に埋もれて、上手く見つけることのできないコアな映画を、効率よく見つけることはできないかと考えたことはありませんか？

このアプリMovieistは、ユーザーの投稿の数だけ映画が更新されていくので、その時の「観たい」をいち早く見つけることができます。
また、投稿するユーザーの為のレビュアーランキングやフォロー機能で、自尊心による投稿意欲をあげ、更新頻度を下げないことで、「観たい」を継続的に見つけることができます。
 
## このアプリを作った理由

このアイデアは、一つの商品から来ています。それは「ポケトーク」という翻訳機です。

スマホの翻訳機能があるにもかかわらず、この商品は出荷台数が80万台を突破するヒット商品になりました。
これをニュースで観た時衝撃を受け、便利な機能を抽出して使いやすくすることで、新しい商品を生み出すことができることを知りました。

そして、その頃使っていた、映画.comというサイトで感じていた、映画情報サイトは映画が主体で、ユーザーの投稿は二の次であるという考えから、
ユーザーの投稿を主体にすることで、投稿者の自尊心をあげ、そこから「観たい」をいち早く見つけることのできるアプリに可能性を感じ、このアプリを作成しました。
 
## 使用技術
 
* Python 3.8.5
* Django 3.2
* Mysql 8.0.23-0ubuntu0.20.04.1
* Vue.js 
* Bootstrap-Vue
* Nginx
* Gunicorn
* AWS
    - EC2
    - VPC
* TMDb API

## AWS構成図
 
## バックエンド機能一覧
* ログイン機能（django-allauth）
* 編集機能
* 投稿機能(django-form)
    - 画像アップロード機能
* Good機能 Bad機能
* ソート機能
* フォロー機能
* ページネーション機能(django.core.paginator)
* 検索機能(TMDb API)
* アラート機能(messages)

## フロントエンド機能一覧
* コメント開閉機能(Vue.js)
* 星評価(vue-star-rating)
* 写真スライド機能(vue-carousel)
* 写真拡大機能(Bootstrap-Vue)
* レスポンシブ機能(Bootstrap-Vue)
