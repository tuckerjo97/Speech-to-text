import datetime, os, logging


class Scraper:
    """With endpoints from crawler, scrap Audio."""
    def __init__(self, relays: list):
        self._relays = relays
        self._logger = logging.getLogger('lofty')

    # Use this for POC, setting id in crawler.py.set_relay()
    def scrap_one(self):
        print(self._relays)
        self._logger.debug('streamripper {} -d ./streams/LAPD Dispatch - Central/ -l 600 -a '.format(self._relays[3]) + 'test_audio_cc')
        os.system('streamripper {} -d ./streams/LAPD Dispatch - Central/ -l 600 -a '.format(self._relays[3]) + "test_audio_cc")

    def scrap_all(self):
        pass

    def fix_above_code(self):  # todo: this is production code, not for testing.
        length = 60 * 60  # 3600 sec
        for (state_id, county, region, feed_id) in self._relays:
            self._logger.debug('streamripper {} -d ./streams/{}/{}/{}/ -l {} -a'.format(
                feed_id, state_id, county, region, length
            ))
            # do same command as debug message.
