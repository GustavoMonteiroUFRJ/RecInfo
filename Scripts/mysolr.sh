#!/bin/bash
if [ "$EUID" -ne 0 ]; then 
    echo "Favor rodar como root"
    echo "sudo ./mysolr.sh"
    exit
fi

install_java()
{
    apt-get update -y
    apt-get install default-jdk -y
}


if type -p java &> /dev/null; then
    version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    if [[ "$version" < "1.8" ]]
    then
        echo Instalando java 8
        install_java
    fi
else
    echo Instalando java
    install_java
fi

if [ ! -d "./solr-8.0.0" ]; then
    echo "Baixando Apache Solr"
    curl "http://ftp.unicamp.br/pub/apache/lucene/solr/8.0.0/solr-8.0.0.tgz" --output ./solr-8.0.0.tgz
    tar -xvzf solr-8.0.0.tgz
    rm solr-8.0.0.tgz
fi

cd ./solr-8.0.0
if ! bin/solr status &> /dev/null; then
    echo Subindo solr na porta 8983
    bin/solr start -c -p 8983 -force
fi

if [ ! -d "./server/solr/configsets/noticias_configs" ]; then
    echo Criando Configs para a colection noticias
    cp -r server/solr/configsets/_default server/solr/configsets/noticias_configs
fi 


if ! curl http://localhost:8983/solr/admin/collections?action=LIST 2> /dev/null | grep noticias &> /dev/null ; then
    echo criando a collections e configura 
    bin/solr create_collection -c noticias -d server/solr/configsets/noticias_configs -n noticias_configs -force
    curl -X POST -H 'Content-type:application/json' --data-binary '{
    "add-field":{
        "name":"text",
        "type":"text_pt",
        "stored":true,
        "indexed":true,
        "uninvertible":true }
    }' http://localhost:8983/solr/noticias/schema

fi

echo Solr no ar!