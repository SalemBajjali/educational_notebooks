from ga4gh.vrs.extras.variation_normalizer_rest_dp import VariationNormalizerRESTDataProxy
from ga4gh.vrs.dataproxy import SeqRepoRESTDataProxy
from ga4gh.vrs.extras.translator import Translator
from api_class import translate_api


class translate_var_from_api:

    def __init__(self):
        """
        Initialize class with the API URL
        """
        
        self.seqrepo_rest_service_url = "https://services.genomicmedlab.org/seqrepo"
        self.dp = SeqRepoRESTDataProxy(base_url=self.seqrepo_rest_service_url)
        self.tlr = Translator(data_proxy=self.dp)
        self.vnorm = VariationNormalizerRESTDataProxy()
        self.api = translate_api()


    def from_spid_to_rightshift_hgvs(self,expression):
        """_summary_

        Args:
            expression (_type_): _description_

        Returns:
            _type_: _description_
        """
        try: 
            # Converting a allele in SPDI syntax to the right-shifted HGVS notation
            return self.api.spdi_to_hgvs(expression)
        except Exception as e: 
            # returns error produce by NCBI API 
            return '{}. Expression Error: {}'.format(e,expression)
        

        
    def from_hgvs_to_spdi(self,expression):
        """_summary_

        Args:
            expression (_type_): _description_

        Returns:
            _type_: _description_
        """
        try: 
            # Converting a allele in SPDI syntax to the right-shifted HGVS notation
            return self.api.hgvs_to_spdi(expression)
        except Exception as e: 
            # returns error produce by NCBI API 
            return '{}. Expression Error: {}'.format(e,expression)  
        


    def to_vrs_object(self,expression):
        """_summary_

        Args:
            expression (_type_): _description_

        Returns:
            _type_: _description_
        """

        api = translate_api()

        try:
            return self.api.variation_to_vrs(expression)
        except Exception as e:
            return '{}. Expression Error: {}'.format(e,expression)  


    def from_vrs_to_normalize_hgvs(self,vrs_object):
        """_summary_

        Args:
            vrs_object (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        pjo = self.tlr.translate_from(vrs_object,"vrs")

        try:
            return self.vnorm.to_hgvs(pjo)[0]
        except Exception as e:
            return '{} Expression Error: {}'.format(e,pjo)  