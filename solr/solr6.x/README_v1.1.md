## ネットワーク作成
NETWORK_NAME=my_network
docker network create $NETWORK_NAME

## Zookeeper起動
### コマンド
ZK_HOST=zk1
ZK_FOWARD_PORT=2181

ZK_IMAGE=jplock/zookeeper
docker pull $ZK_IMAGE

docker create --net $NETWORK_NAME --name $ZK_HOST --hostname=$ZK_HOST -it  -p $ZK_FOWARD_PORT:2181 $ZK_IMAGE
docker start $ZK_HOST

### 参考
https://hub.docker.com/_/zookeeper/

## SolrCloud起動
### イメージPULLコマンド
SOLR_IMAGE=solr:6.6.2
docker pull $SOLR_IMAGE

### znode作成コマンド
docker run --net $NETWORK_NAME -it $SOLR_IMAGE sh server/scripts/cloud-scripts/zkcli.sh -zkhost $ZK_HOST:2181 -cmd makepath /solr

### configアップロードコマンド
CONF_DATA_DIR=xxxx
docker run --net $NETWORK_NAME -v $CONF_DATA_DIR:/tmp/conf -it $SOLR_IMAGE sh
server/scripts/cloud-scripts/zkcli.sh -zkhost zk1:2181/solr -cmd upconfig -confdir /tmp/conf -confname conf01 && exit

### node起動コマンド
SORL_HOST=zksolr1
SORL_PORT=8983

docker create --net $NETWORK_NAME --name $SORL_HOST --hostname=$SORL_HOST -it  -p $SORL_PORT:8983 $SOLR_IMAGE
docker cp $SORL_HOST:/opt/solr/bin/solr.in.sh .
sed -i -e 's/#ZK_HOST=""/ZK_HOST="zk1:2181\/solr"/' solr.in.sh
sed -i -e 's/#*SOLR_HOST=.*/SOLR_HOST="'$SORL_HOST'"/' solr.in.sh
docker cp solr.in.sh $SORL_HOST:/opt/solr/bin/solr.in.sh
rm solr.in.sh
docker start $SORL_HOST

### コレクション作成コマンド
docker exec -i zksolr1 bin/solr create_collection -n config01 -c collection01 -shards 2 -p 8983

### サンプルドキュメント登録コマンド
docker exec -it --user=solr zksolr1 bin/post -c collection01 example/exampledocs/manufacturers.xml

## 作成したネットワークの情報を確認
### コマンド
docker network inspect $NETWORK_NAME

### 参考
https://github.com/docker-solr/docker-solr/blob/master/docs/docker-networking.md
https://lucene.apache.org/solr/guide/6_6/taking-solr-to-production.html
