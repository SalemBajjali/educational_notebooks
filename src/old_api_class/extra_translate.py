from ga4gh.core import ga4gh_digest, ga4gh_identify, ga4gh_serialize
from ga4gh.vrs.dataproxy import SeqRepoRESTDataProxy
import json
from ga4gh.vrs.extras.variation_normalizer_rest_dp import VariationNormalizerRESTDataProxy
from src.old_api_class.variation_services_rest_db import VariationServicesRESTDataProxy
from ga4gh.vrs.extras.translator import Translator
vnorm = VariationNormalizerRESTDataProxy()
vs = VariationServicesRESTDataProxy()


class extra:

    def __init__(self):
        """Initialize class with the seqrepo rest api 
        """
        self.seqrepo_rest_service_url = "https://services.genomicmedlab.org/seqrepo"
        self.dp = SeqRepoRESTDataProxy(base_url=self.seqrepo_rest_service_url)
        self.tlr = Translator(self.dp)


    def to_rightshift_hgvs(self,expression):
        """Converting SPDI allele expression into right shift normalized HGVS expressions.

        Args:
            expression (string): SPDI allele expression 

        Returns:
            string: Right shift normalized HGVS expressions
        """
        
        try: 
            # Converting a allele in SPDI syntax to the right-shifted HGVS notation
            return vs.spdi_to_hgvs(expression)
        except Exception as e: 
            # returns error produce by NCBI API 
            return 'Error in expression {}'.format(e)

    def to_fullynorm_hgvs(self,expression):
        """Converting SPDI allele expression into fully normalized HGVS expressions.

        Args:
            expression (string): SPDI allele expressions

        Returns:
            list: Fully normalized HGVS expressions
        """

        vrs_alleles = []

        try:
            trans = self.tlr.translate_from(expression, 'spdi')
            vrs_alleles.append(trans)
        except Exception as e:
            # returns error produce by translate_from method
            vrs_alleles.append('Error in expression {}'.format(e))

        for allele in vrs_alleles:
            if isinstance(allele, str):
                return allele
            else:
                hgvs_expression = vnorm.to_hgvs(allele, 'refseq')
                return  hgvs_expression

    def to_vrs_allele(self,expression):
        """Convert SPDI allele expression into VRS Allele Object


        Args:
            expression (string): SPDI allele expressions

        Returns:
            dictionary: (Key = ga4gh identifier, Value = VRS allele Object)
        """

        vrs_alleles = {}

        try:
            trans = self.tlr.translate_from(expression)
            vrs_alleles[ga4gh_identify(trans)] = trans.as_dict() #json.dumps(trans.as_dict())
        except Exception as e:
            # returns error produce by translate_from method
            vrs_alleles["Error in expression"] = '{}'.format(e)
            
        return vrs_alleles
    
    # Need to put this function in a different class. Also, don't think functions like this are nessary
    # they constantly need to be reconfigured based off of the dictionary inputed. 
    def create_spdi_expression(self,expression):
        """Takes a spdi dictionary and creates a SPDI allele expression with the follow formate: RefSeq:Posotion:Deletion:Insertion

        Args:
            expression (dictionary): (Key = SPDI four attributes, Values=  Value of each attribute) 

        Returns:
            string: SPDI allele expressions
        """
        # This would change based off of the structure of the dictionary
        spdiobjs = expression['data']['spdis'] 
        for spdiobj in spdiobjs:
            spdi = ':'.join([
                spdiobj['seq_id'],
                str(spdiobj['position']),
                spdiobj['deleted_sequence'],
                spdiobj['inserted_sequence']])
            return spdi




