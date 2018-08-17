# Elastic Issue

> Logstash v6.3.2 기준 (18.08.17) </br>
> ElasticSearch v6.3.2 </br>
> Kibana v6.3.2

### How to MongoDB into Logstash

1. 현재 logstash input-plugin에 mongodb가 없어서 따로 설치해 줘야한다. </br> 아래의 코드를 실행 후, list에  "logstash-input-mongodb" 가 있으면 설치 완료

```
bin/logstash-plugin install logstash-input-mongodb
bin/logstash-plugin list
```

2. MongoDB --> Logstash --> ElasticSearch
> Logstash를 통해 input 값으로 MongoDB 데이터를 받고, output으로 ElasticSearch로 보내기 위한 작업. </br>
> [Logstash Plugin github 참고 ](https://github.com/phutchins/logstash-input-mongodb/blob/master/README.md)

```
# mongodb.config

input {
  mongodb {
   """
   uri : 서버에 있는 mongodb명
   placeholder_db_dir : database 가 저장될 disk 주소 (required)
   placeholder_db_name : placeholder_db_dir 에서 설정한 경로에 생기는 db 명
   collection : mongodb의 collection값
   batch_size : 한 번에 가져올 문서의 배치 크기
   """
    uri => 'mongodb://hostIP:port/mongodb_name'
    placeholder_db_dir => 'C:\USER_PATH\'
    placeholder_db_name => 'mongodb_logstash'
    collection => 'db_collection'
    batch_size => 2000  
  }
}

filter{
   mutate{
       rename => {"_id" => "id"}
   }
}

output{
    elasticsearch{
        hosts => ["localhost:9200"]
    }
}

```
