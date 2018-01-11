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

## ZookeeperコンテナのIP addressを調べる
### コマンド
docker network inspect $NETWORK_NAME

## (途中)SolrCloud起動
### コマンド
ZK1_IP=xxx.xxx.xxx.xxx
SOLR_IMAGE=solr:6.6.2
docker pull $SOLR_IMAGE
HOST_OPTIONS="--add-host zk1:$ZK1_IP"

SORL_HOST=zksolr1
SORL_PORT=8983

docker create --net $NETWORK_NAME --name $SORL_HOST --hostname=$SORL_HOST -it  -p $SORL_PORT:8983 $HOST_OPTIONS $SOLR_IMAGE
docker cp $SORL_HOST:/opt/solr/bin/solr.in.sh .
sed -i -e 's/#ZK_HOST=""/ZK_HOST="zk1:2181"/' solr.in.sh
sed -i -e 's/#*SOLR_HOST=.*/SOLR_HOST="'$SORL_HOST'"/' solr.in.sh
docker cp solr.in.sh $SORL_HOST:/opt/solr/bin/solr.in.sh
rm solr.in.sh
docker start $SORL_HOST


### 参考
https://github.com/docker-solr/docker-solr/blob/master/docs/docker-networking.md
https://lucene.apache.org/solr/guide/6_6/taking-solr-to-production.html


