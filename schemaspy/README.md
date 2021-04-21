# SchemaSpy

[SchemaSpy] is generating your database to HTML documentation, including Entity Relationship diagrams.

## Getting Started

Github 專案  [schemaspy/schemaspy](https://github.com/schemaspy/schemaspy)

### Container version

* schemaspy/schemaspy:6.1.0

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Build docker images and start

配置 data/schemaspy.properties 檔案

```bash
cat data/schemaspy.properties
# type of database. Run with -dbhelp for details
schemaspy.t=mysql
# optional path to alternative jdbc drivers.
#schemaspy.dp=path/to/drivers
# database properties: host, port number, name user, password
schemaspy.host=127.0.0.1
schemaspy.port=3306
schemaspy.db=database
schemaspy.u=user
schemaspy.p=database
# output dir to save generated files
schemaspy.o=/output
# db scheme for which generate diagrams
schemaspy.s=testdb
```

### Start container

啟動 SchemaSpy, 結果會輸出在./data/output中. 完成後可以開啟./output/index.html檢視

```bash
make up
```

### Stop container

```bash
make down
```

清除資料

```bash
make clean
```


[SchemaSpy]: http://schemaspy.org/
