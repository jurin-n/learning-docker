# はじめに
SolrクラスタをDocker使って作ってみました。

# 構成図
TODO

# 参考資料
## Web
Dockerで自由なネットワーク構成を組む https://qiita.com/marufeuille/items/b4065c8756e2a92b18aa
Get started with Docker Machine and a local VM https://docs.docker.com/machine/get-started/
Can I run ZooKeeper and Solr clusters under Docker?　https://github.com/docker-solr/docker-solr/blob/master/Docker-FAQ.md#can-i-run-zookeeper-and-solr-clusters-under-docker
solr image(Docker Hub) https://hub.docker.com/r/_/solr/

## 書籍
Docker実践入門 http://gihyo.jp/book/2015/978-4-7741-7654-3

# 前提環境
$ sw_vers
ProductName:	Mac OS X
ProductVersion:	10.12.6
BuildVersion:	16G29
$ docker --version
Docker version 17.09.0-ce, build afdb6d4
$ virtualbox -h
Oracle VM VirtualBox Manager 5.1.30

# クラスタ作成手順(コマンド)
## VM作成 ＊Windows10の場合は、-dはhyperv にする必要があるらしい。
docker-machine create -d virtualbox solr-vm1


## 作成したVMの環境変数を設定
eval "$(docker-machine env solr-vm1)"

## ネットワーク作成
NETWORK_NAME=my_network
docker network create $NETWORK_NAME

## Zookeeperノード作成
ZK_NAME=zookeeper
docker run --net $NETWORK_NAME --name $ZK_NAME -d -p 2181:2181 -p 2888:2888 -p 3888:3888 jplock/zookeeper

## Solrノード作成(合計４つ)
NODE_NAME=solr1.localhost
HOST_PORT=8983
docker run --net $NETWORK_NAME --name $NODE_NAME -d -p $HOST_PORT:8983 \
      solr:6.6.2 \
      bash -c 'solr start -h '$NODE_NAME' -f -z '$ZK_NAME':2181'

NODE_NAME=solr2.localhost
HOST_PORT=8984
docker run --net $NETWORK_NAME --name $NODE_NAME -d -p $HOST_PORT:8983 \
      solr:6.6.2 \
      bash -c 'solr start -h '$NODE_NAME' -f -z '$ZK_NAME':2181'

NODE_NAME=solr3.localhost
HOST_PORT=8985
docker run --net $NETWORK_NAME --name $NODE_NAME -d -p $HOST_PORT:8983 \
      solr:6.6.2 \
      bash -c 'solr start -h '$NODE_NAME' -f -z '$ZK_NAME':2181'

NODE_NAME=solr4.localhost
HOST_PORT=8986
docker run --net $NETWORK_NAME --name $NODE_NAME -d -p $HOST_PORT:8983 \
      solr:6.6.2 \
      bash -c 'solr start -h '$NODE_NAME' -f -z '$ZK_NAME':2181'

## コレクション作成
NODE_NAME=solr1.localhost
HOST_PORT=8983
docker exec -i -t $NODE_NAME solr create_collection \
        -c item_collection -s 2 -rf 2 -p $HOST_PORT


## 起動中のコンテナに入る
NODE_NAME=solr1.localhost
docker exec -it $NODE_NAME /bin/bash

## 作成したVMで稼働しているSolrコンテナのGUIにアクセス
＊コマンドじゃないので注意。
* docker-machine ip solr-vm1 で作成したVMのIPアドレス調べる
* ブラウザ起動し http://${上記で調べたip}:8983 にアクセス


# 一括削除手順(コマンド)
eval "$(docker-machine env solr-vm1)"
docker stop $(docker ps -q) && docker rm $(docker ps -aq)
docker network rm my_network


# 課題事項
- [ ] 複数VMを跨いだ構成でクラスタ組むこと
- [ ] ホストマシン(Mac)からdocker machineで起動したVMにアクセスできる理由の深堀(ネットワーク的な部分)
- [ ] Solrコンテナの中身(dataファイルのパスとか、dockerfileでどのようにビルドしてるとかなど)
- [ ] Zookeeperコンテナの中身(dataファイルのパスとか、dockerfileでどのようにビルドしてるとかなど)
- [ ] KubernetesとかDocker Swarmとか使ったクラスタ管理基盤の利用
