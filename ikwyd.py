import requests
import lxml.html

# A simple object for storing data about torrents
# TODO add a href to these
class Torrent:
    def __init__(self, first_seen, last_seen, category, title, size):
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.category = category
        self.title = title
        self.size = size
    
    # Used to generate a torrent from a list of strings (from the site)
    @staticmethod
    def from_list(l = list()):
        return Torrent(
            first_seen = l[0], 
            last_seen = l[1],
            category = l[2],
            title = l[3],
            size = l[4]
        )

class RequestFailedException(Exception):
    """Request failed, didn't receive 200 OK!"""

# An object used to scan an IP
class IP:
    # An IP getter
    def get_ip(self):
        return self.__ip
    
    def __init__(self, ip=str()):
        self.__ip = ip

    # Get the URL we should request
    def get_url(self):
        base_url = "https://iknowwhatyoudownload.com/en/peer/"

        return base_url + f"?ip={self.get_ip()}" if len(self.get_ip()) > 0 else base_url

    def __get_torrent_name(self, element):
        return element.getchildren()[0].getchildren()[0].text

    # Gets all of the known torrent downloads for an IP
    def get_torrents(self) -> list():
        # Send the request
        resp = requests.get(
            url = self.get_url(),
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
            }
        )

        # Make sure we are 200 OK
        if not resp.ok:
            raise RequestFailedException(resp)
        
        # Get the response text
        text = resp.text

        # Get the document as an element tree
        etree = lxml.html.fromstring(text)

        # Scan the table
        torrent_elements = etree.xpath("/html/body/div/div/div/div/div[5]/table/tbody/tr")

        torrents = []
        for te in torrent_elements:
            str_components = []
            for part in te:
                # Sometimes the text can be null
                inner_text = str() if part.text == None else part.text

                # Torrent names are handled differently
                if 'class' in part.attrib and part.attrib['class'] == 'name-column':
                    inner_text = self.__get_torrent_name(part)

                # Remove whitespace
                inner_text = inner_text.strip()
                
                # Add it to the list
                str_components.append(inner_text)

            # New torrent!
            torrents.append(Torrent.from_list(str_components))

        return torrents

# TODO Unit test