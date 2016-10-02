### データ専用コンテナビルド
docker build -t dataonly .

### データ専用コンテナ起動
sudo docker run -it --name dataonly dataonly
 *sudoじゃないと起動しなかった。rootで操作してないので、他のコマンドもsudoつけたほうが良いかも。


### docker-compose.ymlで設定したコンテナ類を起動
docker-compose up -d

### Docker Composeで起動したコンテナ群の稼働を一括確認
docker-compose ps
  * 起動している場合は、State列が Up になっている。

### Docker Composeで起動したコンテナ内でコマンドを実行
docker-compose run webserver /bin/sh
  * webserverコンテナでコマンド実行する例

### Docker Composeで起動したコンテナを一括停止
docker-compose stop

### Docker Composeで起動したコンテナを一括で削除
docker-compose rm

### データ専用イメージのバックアップ
docker import backup-data.tar - dataonly
  *dataonlyという名前のコンテナの場合

### データ専用イメージをバックアップからリストア(このやり方うまくいくか怪しい。まだ検証できてない。)
cat backup-data.tar | docker import - dataonly


