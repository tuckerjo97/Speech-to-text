"""
crawls destination website (https://www.broadcastify.com) and gives end-point for Audio scrapping.
These end-points are relay broadcasts, so using stream subscribers (ex. streamripper) are able to listen to it.
"""
from requests_html import HTMLSession
import logging


class Crawler:
    def __init__(self):
        self._session = HTMLSession()
        self._states = []
        self._constants = {
            'STATE_URL': 'https://broadcastify.com/listen/?stid=',
            'BASE_URL': 'https://broadcastify.com/',
            'FEED_URL': 'https://www.broadcastify.com/listen/feed/',
        }
        self._logger = logging.getLogger('lofty')
        self._data = {
            'state_ids': [],
            'feeds': [],
            'relays': []
        }

    def run(self):
        # finding non empty states
        # session = HTMLSession()
        # states = []
        # for stid in range(1, 100):
        #     dest = url + str(stid)
        #     logger.debug(dest)
        #     r = session.get(dest)
        #     messageBox =  r.html.find('.messageBox', first=True)
        #     if messageBox is None:
        #         logger.debug('200 ' + str(count+1))
        #         states.append(stid)
        #
        # logger.debug('Valid state IDs: {}'.format(str(states)))
        #
        pass

    # TODO(sungwon@lofty.ai): This could be hard-coded, but also it could be kept it for scalability.
    def set_state_ids(self) -> None:
        """Fills up self._data['state_ids']."""
        for state_id in range(1, 100):  # Temporal loop, need to be fixed according to above todo.
            dest_url = self._constants['STATE_URL'] + str(state_id)
            try:
                self._logger.debug("Accessing URL: " + dest_url)
                response = self._session.get(dest_url)
                message_box = response.html.find('.messageBox', first=True)
                if message_box is None:
                    self._logger.debug('State id: {} Exists'.format(state_id))
                    self._data['state_ids'].append(state_id )
                    self._logger.debug('States: {}'.format(str(self._data['state_ids'])))

            except Exception as e:  # TODO(sungwon@lofty.ai): read requests_html doc and add exceptions.
                self._logger.error(e)

    def set_feeds(self) -> None:
        """Get URI of feeds"""
        for state_id in self._data['state_ids']:
            response = self._session.get(self._constants['STATE_URL'] + str(state_id))
            self._logger.debug('Connected: {}'.format(self._constants['STATE_URL'] + str(state_id)))
            table = response.html.find('.btable', first=True)
            for tr in table.find('tr'):
                if 'Online' in tr.html and 'Police' in tr.html:  # This logic is temporary.
                    aes = tr.find('a')
                    td = tr.find('td')
                    for a in aes:
                        if 'feed' in a.html:
                            # (state_id, county, region, link)
                            self._logger.debug('Scrapped feeds: {}'.format(str((state_id, td[0].text, td[1].text, a))))
                            self._data['feeds'].append((state_id, td[0].text, td[1].text, a))

    def set_relay(self):
        state_id, county, region, feed_id = 6, 'LA', 'DTLA', 30634
        dest_url = self.feed_url(feed_id=feed_id)
        r = self._session.get(dest_url)
        r.html.render()

        link = r.html.xpath('//*[@id="mep_0"]/div/div[1]') # todo move to constant
        relay = link[0].find('mediaelementwrapper', first=True).find('audio', first=True).attrs['src'] # todo constant.
        self._data['relays'].append((state_id, county, region, relay))

    def set_relays(self):  #production
        pass

    def get_relays(self):
        return self._data['relays']

    def feed_url(self, feed_id) -> str:
        return self._constants['FEED_URL'] + str(feed_id) + '/web'
