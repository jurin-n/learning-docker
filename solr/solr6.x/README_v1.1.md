## Zookeeper起動
### コマンド
docker run --name zk1 --restart always -d -v $(pwd)/zoo_ch08_5.cfg:/conf/zoo.cfg -p2181:2181 zookeeper

### 参考
https://hub.docker.com/_/zookeeper/

## ZookeeperコンテナのIP addressを調べる
### コマンド
docker network inspect bridge

## (途中)SolrCloud起動
### コマンド
docker run --name my_solr -d -p 8983:8983 --add-host zk1:172.17.0.2 -t solr

### 参考
https://github.com/docker-solr/docker-solr/blob/master/docs/docker-networking.md
https://lucene.apache.org/solr/guide/6_6/taking-solr-to-production.html


