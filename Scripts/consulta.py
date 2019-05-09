import pysolr


def define_queries():
    queries = ["text:(+boicote  consumidores~ ! político~)",
               "text:(terrorista~ +ETA && +França~)",
               "text:(filmes documentários Escócia~ gravação~)",
               "text:(+resíduos industriais (métodos remoção))",
               "text:(+desemprego Europa~ números~ taxa~ índice~)",
               "text:('100º aniversário' centenário '100 anos')",
               "text:(+espécies +extinção proteger~ Europa~ animal~)",
               "text:(+greve greve~ causa~ objetivos~ motivo~)",
               "text:(+ópio produção global~ mundial~ cultivo papoilas )",
               "text:(+energia 'crise  energética' energética~ crise combustível~ causa~)"]
    return queries


def get_data(query, host, collection, port=8983):
    path = 'http://{}:{}/solr/{}'.format(host, port, collection)
    solr_client = pysolr.Solr(path)
    return solr_client.search(query, rows=100, fl="* score",df="text")


def fill_file(queries, host, collection, output_file):
    file_write = open(output_file,"w")
    for index in range(0, len(queries)):
        results = get_data(queries[index], host, collection)
        no_rank = 0
        for result in results:
            file_write.write("{} QO {} {} {} GustavoM_Leticia\n".format(index+1,
                                                                      result['id'],
                                                                      no_rank,
                                                                      result['score']))
            no_rank += 1
            if no_rank == 100:
                break
    file_write.close()


queries = define_queries()
fill_file(queries,"localhost","noticias","resultado.txt")
