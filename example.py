"""Example snippets"""
import src.crawler
import src.scraper
import src.preprocess
import src.transcriber
import os


class Example:
    def __init__(self):
        pass

    @staticmethod
    def example():

        # Reason class has methods for each function is for unit testing.
        # Testing is to set your intention in the code, to junior engineer or others understand it.
        # If someone fails the test, they'll know they changed behavior.


        crawler = src.crawler.Crawler()
        crawler.set_state_ids()
        crawler.set_feeds()
        # this is for poc. TODO(sungwon@lofty.ai): refactor when poc moves to production.
        crawler.set_relay()
        relays = crawler.get_relays()[0]
        scraper = src.scraper.Scraper(relays=relays)
        print("starting scrape")
        count = 0
        while count < 6:
            scraper.scrap_one()
            count += 1


        # preprocessor = src.preprocess.Preprocessor("./streams/LAPD/test_audio.mp3", "mp3")
        # preprocessor.remove_silence()
        # files = preprocessor.segments
        #
        # f = open("transcription.txt", "w+")
        # for file in files:
        #     filepath = "segments/" + str(file)
        #     print(filepath)
        #     transcriber = src.transcriber.Transcriber(filepath)
        #     f.write("Transcription for segment " + str(file) + ": " + transcriber.transcribe() + "\n")
        # f.close()



# run here:
example = Example()
example.example()