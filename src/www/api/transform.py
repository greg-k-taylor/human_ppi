# -*- coding: utf-8 -*-
from biothings.web.api.es.transform import ESResultTransformer
from enum import Enum
import logging

class ESResultTransformer(ESResultTransformer):

    # *****************************************************************************
    # Enumerated class for ConsensusPathDB PPI field names
    # *****************************************************************************
    class PpiFields(object):
        CONF = 'interaction_confidence'
        PART = 'interaction_participants'
        PUBS = 'interaction_publications'
        DBS = 'source_databases'

    # *****************************************************************************
    # Safe parse for interaction_confidence
    # *****************************************************************************
    def parse_confidence(self, res, i, hit):
        if self.PpiFields.CONF in hit['_source']:
            val = hit['_source'][self.PpiFields.CONF]
            val = None if (val == "NA" or val == '') else float(val)
            res['hits']['hits'][i]['_source'][self.PpiFields.CONF] = val
        else:
            logging.warning("Field interaction_confidence not returned for this entry.".format(hit['_source']))
            res['hits']['hits'][i]['_source'][self.PpiFields.CONF] = None
        return res

    # *****************************************************************************
    # Safe parse for interaction_participants
    # *****************************************************************************
    def parse_participants(self, res, i, hit):
        # participants - list of strings
        if self.PpiFields.PART in hit['_source']:
            val = hit['_source'][self.PpiFields.PART].replace("_HUMAN", "")
            res['hits']['hits'][i]['_source'][self.PpiFields.PART] = [val] if ',' not in val else val.split(',')
        else:
            logging.warning("Field interaction_participants not returned for this entry - {}".format(hit['_source']))
            res['hits']['hits'][i]['_source'][self.PpiFields.PART] = []
        return res

    # *****************************************************************************
    # Safe parse for interaction_publications
    # *****************************************************************************
    def parse_publications(self, res, i, hit):
        # publications - list of integers
        if self.PpiFields.PUBS in hit['_source']:
            val = hit['_source'][self.PpiFields.PUBS]
            pubs_strs = [val] if ',' not in val else val.split(',')
            try:
                pubs_ints = list(map(int, pubs_strs))
            except ValueError:
                pubs_ints = []
                logging.warning("Publication Entry for this query is not valid - {}".format(pubs_strs))
            res['hits']['hits'][i]['_source'][self.PpiFields.PUBS] = pubs_ints
        else:
            logging.warning("Field interaction_publications not returned for this entry - {}".format(hit['_source']))
            res['hits']['hits'][i]['_source'][self.PpiFields.PUBS] = []
        return res

    # *****************************************************************************
    # Safe parse for source_databases
    # *****************************************************************************
    def parse_databases(self, res, i, hit):
        # databases - list of strings
        if self.PpiFields.DBS in hit['_source']:
            val = hit['_source'][self.PpiFields.DBS]
            res['hits']['hits'][i]['_source'][self.PpiFields.DBS] = [val] if ',' not in val else val.split(',')
        else:
            logging.warning("Field source_databases not returned for this entry - {}".format(hit['_source']))
            res['hits']['hits'][i]['_source'][self.PpiFields.DBS] = []
        return res

    # #############################################################################
    # Add Human_PPI specific result transformations for query results
    # #############################################################################
    def clean_query_GET_response(self, res):
        logging.info("Query transformation call on {} hits".format(len(res['hits']['hits'])))

        for i, hit in enumerate(res['hits']['hits']):
            res = self.parse_confidence(res, i, hit)
            res = self.parse_participants(res, i, hit)
            res = self.parse_publications(res, i, hit)
            res = self.parse_databases(res, i, hit)
        return res
