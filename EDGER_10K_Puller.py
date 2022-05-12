
try: 
    from sec_api import QueryApi
    from sec_api import ExtractorApi
except ImportError:
    import pip 
    pip.main(['install', 'sec_api'])
    from sec_api import QueryApi
    from sec_api import ExtractorApi
import json


"""
File_10k_Puller:
    Inputs: 
        ticker (string): Ticker of company 
        start date (string 'YYYY-MM-DD'): Date where the search query will begin
        end date (string 'YYYY-MM-DD'): Date where the search query will end
        api_key (string): sec-api key (obtained from https://sec-api.io/signup/free)
    
    Methods:
        get_10k_query
            Inputs: 
                self
            Returns: 
                Returns a query according to the search parameters defined in __init__
        
        get_10k_link
            Inputs:
                self 
            Returns 
                {date of filing: filing url}

        get_10k_text
            Inputs:
                self 
                url (string): document url sourced from get_10k_link
                section_codes (list): Sections of 10-k to include in the output. 
                                        When set to default (None), function will return all sections included in the 10-k

            Returns: 
                {Section name:[section_code,text]}
        
        fill_json
            Inputs:
                self
                section_codes (list): codes to include in final output. When set to default (None), function will 
                                      return all sections included in the 10-k
            Returns: 
                Saves file in directory in json format using the ticker as the file name

"""
class File_10k_Puller: 
    def __init__(self, ticker,start_date, end_date, api_key): 
        self.__ticker = ticker 
        self.__start_date = start_date
        self.__end_date = end_date
        self.__api_key = api_key

    #get query of filings
    def get_10k_query(self):
        ticker = self.__ticker
        start_date = self.__start_date 
        end_date = self.__end_date
        info_string = "ticker:"+ticker+" AND filedAt:{"+start_date+" TO "+end_date+"} AND formType:\"10-K\""
        queryApi = QueryApi(api_key=self.__api_key)
        query = {
                    "query": { "query_string": { 
                        "query": info_string
                        } },
                    "from": "0",
                    "size": "10",
                    "sort": [{ "filedAt": { "order": "desc" } }]
                    }

        return queryApi.get_filings(query)

    #get linkns to 10-k filing
    def get_10k_link(self): 
        query = self.get_10k_query()
        link_map = dict()

        for n in range(len(query['filings'])): 
            link_to_filing = query['filings'][n]['linkToFilingDetails']
            date = query['filings'][n]['filedAt']
            link_map[date] = link_to_filing

        return link_map

    #returns the text of a section in the 10-K
    #save_file = True saves the text into a json file in the wokring directory
    #sections are consitent: https://www.sec.gov/fast-answers/answersreada10khtm.html
    def get_10k_text(self, url, section_codes = None,):
        extractorApi = ExtractorApi(self.__api_key)
        section_map = {'Buisness': '1',
                        'Risk Factors': '1A',
                        'Unresolved Staff Comments': '1B',
                        'Properties': '2',
                        'Legal Proceedings': '3',
                        'Mine Safety Disclosures':'4',
                        'Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities': '5',
                        'Management’s Discussion and Analysis of Financial Condition and Results of Operations':'7',
                        'Quantitative and Qualitative Disclosures about Market Risk': '7A',
                        'Financial Statements and Supplementary Data':'8',
                        'Changes in and Disagreements with Accountants on Accounting and Financial Disclosure': '9',
                        'Controls and Procedures': '9A',
                        'Other Information': '9B',
                        'Directors, Executive Officers and Corporate Governance': '10',
                        'Executive Compensation': '11',
                        'Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters': '12',
                        'Certain Relationships and Related Transactions, and Director Independence': '13',
                        'Principal Accountant Fees and Services': '14',
                        'Exhibits, Financial Statement Schedules': '15'
                        }

        out_dict = dict()

        #pulls all sections in section map
        if section_codes == None: 
            for section in section_map.keys():
                section_code = section_map[section]
                try: 
                    section_text = extractorApi.get_section(url, section_code, "text") 
                    out_dict[section] = [section_code,section_text]
                except: #handle exception when the section is not in the 10-K
                    print('===================================')
                    print('Warning: section not available for section ',section_code)
                    print('===================================')

        #pulls only user selected sections when section_codes != none
        else: 
            for section_code in section_codes:
                try:
                    section_name = None #default value incase section_code input is not valid 
                    for section in section_map.keys():
                        if section_map[section] == section_code:
                            section_name = section
                    section_text = extractorApi.get_section(url, section_code, "text")
                    out_dict[section_name] = [section_code,section_text]
                except: #handle exception when the section is not in the 10-K
                    print('===================================')
                    print('Warning: section not available for section ',section_code)
                    print('===================================')

        return out_dict

    #create a json file of all the filings pulled through def get_10k_link
    #only gets whatever section is inputted into get_10k_text
    def pull_file(self, section_codes): 
        link_map = self.get_10k_link()
        out_dict = dict()
        out_dict[self.__ticker] = dict()
        for date in link_map.keys(): 
            url = link_map[date]
            text_dict = self.get_10k_text(url,section_codes)
            out_dict[date] = text_dict

        return out_dict
