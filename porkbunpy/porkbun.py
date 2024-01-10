import requests


class DnsRecord:
    """
    DNS record of a given domain
    """
    def __init__(self, domain, name: str, record_type: str, content: str, session):
        self.domain = domain
        self.name = name
        self.record_type = record_type
        self.content = content
        
        self.record = name.replace(f".{domain}", '') if domain != name else name

        self.session = session


    def edit_content(self, content: str):
        """
        Edit the content of a DNS record
        """
        URL = self.session['base_url'] + f"dns/editByNameType/{self.domain}/{self.record_type}/{self.record}"
        DATA = {
            'secretapikey': self.session['secret_api_key'],
            'apikey': self.session['api_key'],
            "content": content
        }
        response = requests.post(url=URL, json=DATA)
        return response.json()


class Domain:
    def __init__(self, domain: str, tld: str, session):
        self.domain = domain
        self.tld = tld

        self.session = session


    def get_records(self) -> list[DnsRecord] | None:
        URL = self.session['base_url'] + f"dns/retrieve/{self.domain}"
        REQUEST_DATA = {
            'secretapikey': self.session['secret_api_key'],
            'apikey': self.session['api_key'] 
        }

        response = requests.post(url=URL, json=REQUEST_DATA).json()
        
        records_to_return = []
        if 'records' in response:
            for record in response['records']:
                records_to_return.append(DnsRecord(
                    domain=self.domain,
                    name=record['name'],
                    record_type=record['type'],
                    content=record['content'],
                    session=self.session
                ))

            return records_to_return
        else:
            raise Exception("Could not retrieve records list" + response["message"])

    
    def get_record_by_name(self, name: str):
        records = self.get_records()
        if records is not None:
            for record in records:
                if record.record == name:
                    return record


class Porkbun:
    def __init__(self, api_key: str, secret_api_key: str):
        self.URL = 'https://porkbun.com/api/json/v3/'
        self.api_key = api_key
        self.secret_api_key = secret_api_key


    def get_domains(self) -> list[Domain]:
        """
        Get domains by user
        """
        DOMAINS_URL = self.URL + "domain/listAll"
        
        REQUEST_DATA = {
            "secretapikey": self.secret_api_key,
            "apikey": self.api_key
        }

        response: dict = requests.post(url=DOMAINS_URL, json=REQUEST_DATA).json()
        
        domains_to_return = []
        
        if "domains" in response:
            for domain in response['domains']:
                domains_to_return.append(Domain(
                    domain=domain['domain'],
                    tld=domain['tld'],
                    session={'api_key': self.api_key, 'secret_api_key': self.secret_api_key, 'base_url': self.URL}
                ))
            
            return domains_to_return
        else:
            raise Exception("Could not retrieve the domains list for the given credentials ")


    def get_domain_by_name(self, name: str) -> Domain | None:
        domains = self.get_domains()
        for domain in domains:
            if domain.domain == name:
                return domain

