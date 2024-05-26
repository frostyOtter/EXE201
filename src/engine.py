# load libraries
import elasticsearch
from loguru import logger

class SearchEngine:
    def __init__(self, id_name:str, api_key:str, index_name:str)->None:
        # init client
        self.client = elasticsearch.Elasticsearch(
                cloud_id= id_name,
                api_key= api_key
            )

        self.index_name = index_name

    def search_one_feature(self, input_query:str, input_feature:str)->dict:
        response = self.client.search(
            index= self.index_name,
            query={"match": {input_feature: {"query": input_query}}}
        )
        if len(response["hits"]["hits"]) == 0:
            logger.debug(f"Your search in {input_feature} returned no results, query: {input_query}")
            return {}
        else:
            response = response["hits"]["hits"]

        return response


    def search_many_feature(self, input_query:str, input_features:list)->dict:
        if not isinstance(input_features, list):
            logger.debug("features input must be in a list")
            return {}
        if len(input_features) == 1:
            logger.debug("Use search_one_feature if searching a single field.")
            return {}
        
        response = self.client.search(
                index= self.index_name,
                query={"multi_match": {"query": input_query, "fields": input_features}},
                )
        if len(response["hits"]["hits"]) == 0:
            logger.debug(f"Your search in {input_features} returned no results, query: {input_query}")
            return {}
        else:
            response = response["hits"]["hits"]
            
        return response
    
    def delete_one_record(self, input_feature:str):
        pass