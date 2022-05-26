import json
import requests
from bs4 import BeautifulSoup
from typing import Any

class CarHistory:
    BASE_URL = """https://historiapojazdu.gov.pl/strona-glowna/-/hipo/historiaPojazdu/dynaTraceMonitor?type=js&session=6FBAF754694A80A9CA7E1A3C506ABEDD|SGlzdG9yaWErUG9qYXpkdXwx&flavor=post&referer=https://historiapojazdu.gov.pl/strona-glowna/-/hipo/historiaPojazdu/cepik?p_auth=BGU1cYEX&modifiedSince=1626785985775&app=Historia Pojazdu"""
    
    def __init__(self, plate: str, vin: str, date: str) -> None:
        self.plate = plate
        self.vin = vin
        self.fr_date = date # date of first registration
        self.info = {}
        self.soup: BeautifulSoup
    
    def to_json(self) -> None:
        with open('data.json', 'w') as fp:
            json.dump(self.info, fp, indent=4, ensure_ascii=False)
            
    def get_info(self) -> dict[str, Any]:
        return self.info
        
    def _info_to_json(self):
        return json.dumps(self.info)    
        
    def get_car_history(self) -> None:
        try:
            self._get_content()
        except Exception as error:
            print("Error in scraper", error) 
        self._scrap_basic_info()
        self._scrap_tech_data()
        self._scrap_history_table()
        self.to_json()
        return self._info_to_json()
        
        
    def _get_content(self) -> None:
        
        payload = {
            '_historiapojazduportlet_WAR_historiapojazduportlet_:formularz':"_historiapojazduportlet_WAR_historiapojazduportlet_:formularz",
            'javax.faces.encodedURL': "https://historiapojazdu.gov.pl/strona-glowna?p_p_id=historiapojazduportlet_WAR_historiapojazduportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_historiapojazduportlet_WAR_historiapojazduportlet__jsfBridgeAjax=true&_historiapojazduportlet_WAR_historiapojazduportlet__facesViewIdResource=%2Fviews%2Findex.xhtml",
            '_historiapojazduportlet_WAR_historiapojazduportlet_:rej': self.plate,
            '_historiapojazduportlet_WAR_historiapojazduportlet_:vin': self.vin,
            '_historiapojazduportlet_WAR_historiapojazduportlet_:data': self.fr_date,
            '_historiapojazduportlet_WAR_historiapojazduportlet_': "btnSprawdz: Sprawdź+pojazd+»",
            'javax.faces.ViewState': "-8249950652064489689:7429482080796207134"
        }
        
        # response = requests.post(url=self.BASE_URL, data=payload)
        # soup = BeautifulSoup(response, 'html.parser')    
        soup = BeautifulSoup(open('index.html'), 'html.parser')
        self.soup = soup
    
    def _scrap_basic_info(self) -> None:
        soup = self.soup.find('div', {'id': 'dane-podstawowe'}).find_all("p")
        info_dict = {}
        for p in soup:
            info_dict[p['class'][0]] = p.span.string
        self.info['Dane podstawowe'] = info_dict
        
    def _scrap_tech_data(self) -> None:
        soup = self.soup.find('section', {'class': 'box-information', 'aria-label': 'Raport - informacje techniczne'})
        items = soup.find_all('div', {"class":"item"})
        for item in items:
            info_dict = {}
            name = item.find('h2').string
            for p in item.find_all("p"):
                spans = p.find_all('span')
                info_dict[spans[0].string.strip().replace(":", "")] = spans[1].string.strip()
            self.info[name] = info_dict

    def _scrap_history_table(self):
        soup = self.soup.find('table', {'id':'timeline'}).find_all('tr')
        info_dict = {}
        for tr in soup:
            try:
                key = tr.find('td', {'class': 'date'}).find('p').string.strip()
                value = tr.find('td', {'class': 'description'})
                checkpoint_dict = {}
                checkpoint_dict['info'] = value.find('p').string.strip()
                for p in value.find_all('p'):
                    items = p.find_all('span')
                    if len(items) > 1:
                        checkpoint_dict[items[0].string] = items[-1].string
                info_dict[key] = checkpoint_dict
            except AttributeError as error:
                print(error)
                pass
        self.info["Oś czasu"] = info_dict

if __name__ == "__main__":
    
    autko = CarHistory('', '', '')
    autko.get_car_history()