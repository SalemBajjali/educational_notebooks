import re 

class spdi_expression:

    def validate_spdi(self,expression):
        spdi_re = re.compile(r"(?P<ac>[^:]+):(?P<pos>\d+):(?P<del_len_or_seq>\w*):(?P<ins_seq>\w*)")

        ismatch = spdi_re.match(expression)
        if ismatch == None:
            return 'SPDI syntax does not match regular expression'

        return expression  

    def spdi_dictionary(self,expression):   
            seq_id,position,deletion,insertion = expression.split(':')

            spdi_dict = {
                'seq_id': seq_id,
                'position': position,
                'deletion': deletion,
                'insertion': insertion
            }

            return spdi_dict
    
    def spdi_list(self,expression):
        mylist = []
        mylist.append(expression.split(':'))
        return mylist 
    
# class spdi_attributes:

    def create_spdi_expression(self,attribute_list):
        spdi_re = re.compile(r"(?P<ac>[^:]+):(?P<pos>\d+):(?P<del_len_or_seq>\w*):(?P<ins_seq>\w*)")
        spdi = ':'.join(attribute_list)
        ismatch = spdi_re.match(spdi)
        if ismatch == None:
            return 'SPDI syntax does not match regular expression'
        return spdi
    
    def create_spdi_dictionary(self,attribute_list):
        spdi_dict = {
            'seq_id': attribute_list[0],
            'position': attribute_list[1],
            'deletion': attribute_list[2],
            'insertion': attribute_list[3]
        }
        return spdi_dict

    def spdi_expression_from_dictionary(self,spdi_dictionary):
        spdi = ':'.join([
            spdi_dictionary['seq_id'],
            str(spdi_dictionary['position']),
            spdi_dictionary['deletion'],
            spdi_dictionary['insertion']])
        return spdi
    
# class spdi_expression():

#     def __init__(self,expression):
#         self.expression = expression

#     def validate_spdi(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """
#         spdi_re = re.compile(r"(?P<ac>[^:]+):(?P<pos>\d+):(?P<del_len_or_seq>\w*):(?P<ins_seq>\w*)")

#         ismatch = spdi_re.match(self.expression)
#         if ismatch == None:
#             return 'SPDI syntax does not match regular expression'

#         return self.expression  

#     def spdi_dictionary(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """
#         try:
#             return self.validate_spdi()
#         except:
#             seq_id,position,deletion,insertion = self.expression.split(':')

#             spdi_dict = {
#                 'seq_id': seq_id,
#                 'position': position,
#                 'deletion': deletion,
#                 'insertion': insertion
#             }

#             return spdi_dict
    
#     def spdi_list(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """
#         try:
#             return self.validate_spdi()
#         except:
#             mylist = []
#             mylist.append(self.expression.split(':'))
#             return mylist 
    
# class spdi_attributes():

#     def __init__(self,sequence,position:int,deletion,insertion):
#         self.sequence = sequence
#         self.position = position
#         self.deletion = deletion
#         self.insertion = insertion

#     def spdi_expression(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """
#         spdi_re = re.compile(r"(?P<ac>[^:]+):(?P<pos>\d+):(?P<del_len_or_seq>\w*):(?P<ins_seq>\w*)")
        
#         spdi = ':'.join([self.sequence,str(self.position),self.deletion,self.insertion])
        
#         ismatch = spdi_re.match(spdi)
#         if ismatch == None:
#             return 'SPDI syntax does not match regular expression'
    
#         return spdi

#     def create_spdi_dictionary(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """

#         spdi_dict = {
#             'seq_id': self.sequence,
#             'position': self.position,
#             'deletion': self.deletion,
#             'insertion': self.insertion
#         }

#         return spdi_dict

#     def spdi_expression_from_dictionary(self,spdi_dictionary):
#         """_summary_

#         Args:
#             spdi_dictionary (_type_): _description_

#         Returns:
#             _type_: _description_
#         """
#         spdi = ':'.join([
#             spdi_dictionary['seq_id'],
#             str(spdi_dictionary['position']),
#             spdi_dictionary['deletion'],
#             spdi_dictionary['insertion']])
#         return spdi
    

if __name__ in '__main__':

    exp = spdi_expression('NC_000001.10:12344:T:A')
    print(exp.spdi_dictionary())
    # print(exp.spdi_list())

    # atr_exp = spdi_attributes('NC_000001.10',12344,'T','A')
    # print(atr_exp.spdi_expression())
    # print(atr_exp.create_spdi_dictionary())
    # test = atr_exp.create_spdi_dictionary()
    # print(atr_exp.spdi_expression_from_dictionary(test))
