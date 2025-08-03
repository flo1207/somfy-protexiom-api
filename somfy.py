from bs4 import BeautifulSoup
import requests, re, json, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SomfyException(Exception):
    pass

# Main class to interact with the Somfy web interface
class Somfy:
    def __init__(self, url, password, codes):
        self.url = url # Base URL of the Somfy device
        self.password = password # Password for login
        self.codes = codes # Dictionary of authentication keys
        self.session = requests.Session() # Persistent HTTP session
        self.session.verify = False # Disable SSL verification

    # Context manager entry (for use with 'with' statement)  
    def __enter__(self):
        self.login() # Automatically login
        return self

    # Context manager exit (auto logout)
    def __exit__(self, type, value, traceback):
        self.logout()

    # Login method: extract code from login page and authenticate
    def login(self):
        response = self.session.get(f"{self.url}/fr/login.htm")
        soup = BeautifulSoup(response.content, "lxml")
     
        form = soup.find('form')
        if not form:
            raise SomfyException("Login form not found")

        table = form.find('table')
        if not table:
            raise SomfyException("Table not found in login form")

        tr_tags = table.find_all('tr')
        if len(tr_tags) <= 2:
            raise SomfyException("Not enough rows in the login form table")

        b_tags = tr_tags[2].find_all('b')
        if not b_tags:
            raise SomfyException("Authentication code not found")

        auth_code = b_tags[0].get_text()
        key = f"key_{auth_code}"
        payload = {
            "login": "u", # Default login
            "password": self.password,
            "key": self.codes.get(key), # Lookup one-time code
            "btn_login": "Connexion"
        }

        if payload["key"] is None:
            raise SomfyException("Invalid authentication code")
        
        # Submit login form
        self.session.post(f"{self.url}/fr/login.htm", data=payload)

    # Logout method
    def logout(self):
        self.session.get(f"{self.url}/logout.htm")

    # Turn on all zones A, B, and C
    def set_zone(self, zone):
        payload = {
            "hidden": "hidden",
            "btn_zone_on_ABC": "Marche A B C"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)
    
    # Turn off all zones A, B, and C
    def unset_all_zones(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_off_ABC": "Arrêt A B C"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Turn on zone A
    def set_A(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_on_A": "Marche A"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Turn on zone B
    def set_B(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_on_B": "Marche B"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Turn on zone C
    def set_C(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_on_C": "Marche C"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Turn off zone A
    def unset_A(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_off_A": "Arrêt A"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Turn off zone B
    def unset_B(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_off_B": "Arrêt B"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Turn off zone C
    def unset_C(self):
        payload = {
            "hidden": "hidden",
            "btn_zone_off_C": "Arrêt C"
        }
        self.session.post(f"{self.url}/fr/u_pilotage.htm", data=payload)

    # Get overall system state (e.g., battery, door status, etc.)
    def get_state(self):
        response = self.session.get(f"{self.url}/fr/u_pilotage.htm")
        soup = BeautifulSoup(response.content, "lxml")
        state = self._parse_general_state(soup)
        return state
    
    # Get alarm state per zone (A, B, C)
    def get_alarme_state(self):
        response = self.session.get(f"{self.url}/fr/u_pilotage.htm")
        soup = BeautifulSoup(response.content, "lxml")
        state = self._parse_zone_state(soup)
        return state
    
    # Parse the state of each alarm zone (groupa, groupb, groupc)
    def _parse_zone_state(self, soup):
        group_state = soup.find("div", id="groupstate")
        if not group_state:
            raise SomfyException("Group state section not found")

        # Dictionary with initial empty values for group states
        group_mapping = {
            "groupa": {"etat":"","info":""},
            "groupb": {"etat":"","info":""},
            "groupc": {"etat":"","info":""}
        }

        # Initialiser result avec les mêmes clés que group_mapping
        result = {key: {"etat": "", "info": ""} for key in group_mapping}
        
        for key in group_mapping:
            state_div = group_state.find("div", id=key)
            if state_div:
                state = state_div.find("div", class_="alarmoff") or state_div.find("div", class_="alarmon")
                info = state_div.find("div", class_="noalarm") or state_div.find("div", class_="alarm")

                if state:
                    result[key]["etat"] = state.get_text(strip=True)
                else:
                    result[key]["etat"] = "État non trouvé"

                if info:
                    result[key]["info"] = info.get_text(strip=True)
                else:
                    result[key]["info"] = "Info non trouvée"
            else:
                result[key] = {"etat": "Groupe non trouvé", "info": "Groupe non trouvé"}

        return result

    # Parse general system status (battery, communication, GSM, etc.)
    def _parse_general_state(self, soup):
        alarm_state = soup.find("div", id="alarmstate")
        if not alarm_state:
            raise SomfyException("Alarm state section not found")

        # Dictionary with empty values for keys
        state_mapping = {
            "pbattery_nok": "",
            "pcom_nok": "",
            "pdoor_nok": "",
            "phouse_ok": "",
            "pbox_ok": "",
            "pgsm_5_ok": "",
            "pcam_off": ""
        }

        general_state = {}

        for class_name, description in state_mapping.items():
            general_state[class_name] = description

        # Find all divs whose class starts with 'p'
        div_elements = alarm_state.find_all("div", class_=re.compile(r'\bp.*?\b'))  # Find all divs with class starting with 'p'
        for div in div_elements:
            class_name = div.get("class")[0]  # Get the first class of the div
            description = div.get_text(strip=True)  # Get the text content of the div
            if class_name in general_state:
                general_state[class_name] = description

        return general_state

    # Helper to beautify and check for HTML errors  
    def _beautiful_it_and_check_error(self, html):
        soup = BeautifulSoup(html, "lxml")
        self._check_error(soup)
        return soup

    # Detect errors on page and raise appropriate exceptions
    def _check_error(self, soup):
        error_div = soup.find("div", {"class": "error"})
        if error_div:
            error_code = error_div.find('b').get_text()
            error_messages = {
                '(0x0904)': "Maximum attempts reached",
                '(0x1100)': "Incorrect code",
                '(0x0902)': "Session already open",
                '(0x0812)': "Wrong login/password",
                '(0x0903)': "Insufficient access rights"
            }
            raise SomfyException(error_messages.get(error_code, "Unknown error"))
