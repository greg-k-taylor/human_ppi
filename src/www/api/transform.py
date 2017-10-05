# -*- coding: utf-8 -*-
from biothings.web.api.es.transform import ESResultTransformer
from enum import Enum
import logging

class ESResultTransformer(ESResultTransformer):

    class PPIFields(Enum):
        CONF = 'interaction_confidence'
        PARTICIPANTS = 'interaction_participants'
        PUBS = 'interaction_publications'
        DBS = 'source_databases'

    # Add Human_PPI specific result transformations
    def clean_query_GET_response(self, res):
        logging.debug("GREG-BEFORE - {}".format(res))
        for i, hit in enumerate(res['hits']['hits']):

            # confidence
            val = hit['_source']['interaction_confidence']
            val = None if val == "NA" else float(val)
            res['hits']['hits'][i]['_source']['interaction_confidence'] = val

            # participants - list of strings
            val = hit['_source']['interaction_participants'].replace("_HUMAN", "")
            res['hits']['hits'][i]['_source']['interaction_participants'] = [val] if ',' not in val else val.split(',')

            # publications - list of integers
            val = hit['_source']['interaction_publications']
            pubs_strs = [val] if ',' not in val else val.split(',')
            res['hits']['hits'][i]['_source']['interaction_publications'] = list(map(int, pubs_strs))

            # databases - list of strings
            val = hit['_source']['source_databases']
            res['hits']['hits'][i]['_source']['source_databases'] = [val] if ',' not in val else val.split(',')

            logging.debug("{} - {}".format(i, res['hits']['hits'][i]['_source']['interaction_confidence']))
        logging.debug("GREG-AFTER - {}".format(res))

        return res
