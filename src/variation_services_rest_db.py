import requests
import json
import sys


# Citation: 
    # https://ngdc.cncb.ac.cn/gwh/assembly/history
    # https://api.ncbi.nlm.nih.gov/variation/v0/
    # https://github.com/ncbi/dbsnp
    # https://github.com/ncbi/dbsnp/blob/master/tutorials/Variation%20Services/Jupyter_Notebook/spdi_batch.ipynb
    # https://github.com/ga4gh/vrs-python/blob/main/src/ga4gh/vrs/extras/variation_normalizer_rest_dp.py


class VariationServicesRESTDataProxy:
    """
    Rest data proxy for Variation Services API
    """

    def __init__(self):
        """
        Initialize class with the API URL
        """
        
        self.api = 'https://api.ncbi.nlm.nih.gov/variation/v0/'

    def spdi_syntex(self,r):
        """ 
        Extract spdi attributes,and concatinating the attirbutes to create a spdi syntax allele. 
        """

        reqjson = json.loads(r.text)
        spdiobjs = reqjson['data']['spdis'] #[0] Index at first position for the first spdi object. 
        expr_list = []
        for spdiobj in spdiobjs:
            spdi = ':'.join([
                spdiobj['seq_id'],
                str(spdiobj['position']),
                spdiobj['deleted_sequence'],
                spdiobj['inserted_sequence']])
            expr_list.append(spdi)
        return expr_list

    def spdi_to_hgvs(self,spdi_expr):
        """ Translate contextual allele in spdi syntax to right-shfted hgvs notation.
            End point used from variation service api: /spdi/{spdi}/hgvs

        Args:
            spdi_expr (string):SPDI allele expression 

        Returns:
            string: Right shfted hgvs notation
        """
        r = requests.get(
            url = "{}spdi/{}/hgvs".format(self.api,spdi_expr),
            headers={ "Content-Type": "application/json; charset=utf-8" }
        )

        if r.status_code == 200:
            return json.loads(r.text)['data']['hgvs'] 
        else:
            raise requests.HTTPError(f"Variation Services returned the status code: {r.status_code}.")

    def hgvs_to_spdi(self,hgvs_expr, assembly ='GCF_000001405.38'): 
        """Translate hgvs notation to contextual allele in spdi syntax.
           End point used from variation service api: /hgvs/{hgvs}/contextuals 

        Args:
            hgvs_expr (string): hgvs notation
            assembly (str): Default assembely. Defaults to 'GCF_000001405.38'.

        Returns:
            list: contextual allele in spdi syntax
        """
        #TODO: double check if this returns a list

        
        r = requests.get(
            url = "{}hgvs/{}/contextuals?assembly={}".format(self.api,hgvs_expr,assembly),
            headers={ "Content-Type": "application/json; charset=utf-8" }
        )

        if r.status_code == 200:
            return self.spdi_syntex(r)
        else:
            raise requests.HTTPError(f"Variation Services returned the status code: {r.status_code}.")
