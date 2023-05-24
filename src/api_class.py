# Citation: 
    # https://ngdc.cncb.ac.cn/gwh/assembly/history
    # https://api.ncbi.nlm.nih.gov/variation/v0/
    # https://github.com/ncbi/dbsnp
    # https://github.com/ncbi/dbsnp/blob/master/tutorials/Variation%20Services/Jupyter_Notebook/spdi_batch.ipynb
    # https://github.com/ga4gh/vrs-python/blob/main/src/ga4gh/vrs/extras/variation_normalizer_rest_dp.py


# Packages imported

# First Part
import requests
import json

class translate_api:

    def __init__(self):
        """
        Initialize class with the API URL
        """
        
        self.base_ncbi_url_api = 'https://api.ncbi.nlm.nih.gov/variation/v0/'
        self.base_varnorm_url_api = 'https://normalize.cancervariants.org'

        self.headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

    def variation_to_vrs(self,q, untranslatable_returns_text='true'):
        """_summary_

        Args:
            q (_type_): _description_
            untranslatable_returns_text (str, optional): _description_. Defaults to 'true'.

        Raises:
            requests.HTTPError: _description_

        Returns:
            _type_: _description_
        """
        
        endpoint = '/variation/to_vrs'

        url = f'{self.base_varnorm_url_api}{endpoint}'
        
        params = {
            'q': q,
            'untranslatable_returns_text': untranslatable_returns_text
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        
        if response.status_code == 200:
            return json.loads(response.text)['variations'][0]
        else:
            raise requests.HTTPError(f'Request failed with status code: {response.status_code}')

    def spdi_attribute_concat(self,r):
        """_summary_

        Args:
            r (_type_): _description_

        Returns:
            _type_: _description_
        """

        """ 
        Extract spdi attributes,and concatenating the attributes to create a spdi syntax allele. 
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

    def spdi_to_hgvs(self,spdi_id):
        """_summary_

        Args:
            spdi_id (_type_): _description_

        Raises:
            requests.HTTPError: _description_

        Returns:
            _type_: _description_
        """

        endpoint = '/spdi/{}/hgvs'.format(spdi_id)
        
        url = f'{self.base_ncbi_url_api}{endpoint}'

        
        response = requests.get(url,headers=self.headers)

        if response.status_code == 200:
            return json.loads(response.text)['data']['hgvs']
        else:
            raise requests.HTTPError(f'Request failed with status code: {response.status_code}')
        
    def hgvs_to_spdi(self,hgvs_id, assembly ='GCF_000001405.38'):
        """_summary_

        Args:
            hgvs_id (_type_): _description_
            assembly (str, optional): _description_. Defaults to 'GCF_000001405.38'.

        Raises:
            requests.HTTPError: _description_

        Returns:
            _type_: _description_
        """

        """_summary_

        Args:
            hgvs_id (_type_): _description_
            assembly (str, optional): _description_. Defaults to 'GCF_000001405.38'.

        Raises:
            requests.HTTPError: _description_

        Returns:
            _type_: _description_
        """

        endpoint = '/hgvs/{}/contextuals{}'.format(hgvs_id,assembly)
        
        url = f'{self.base_ncbi_url_api}{endpoint}' 

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return self.spdi_attribute_concat(response)[0] # if I only want back one spdi expression [0]
        else:
            raise requests.HTTPError(f'Request failed with status code: {response.status_code}')
    
