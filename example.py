"""Example snippets"""
import src.crawler
import src.scraper
import src.preprocess
import src.transcriber
import src.parser
import os
import pydub

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

        # Scrape an hour in 10 min segments
        while count < 6:
            scraper.scrap_one()
            count += 1

        # Convert mp3 files to wav files
        for j in range(6):
            if j == 0:
                filename = "streams/LAPD/test_audio_cc.mp3"
            else:
                filename = "streams/LAPD/test_audio_cc ({}).mp3".format(j)
            preprocess.convert_mp3_to_wav(audio_path=filename)

        if j == 0:
            filename = "streams/LAPD/test_audio_cc.wav"
        else:
            filename = "streams/LAPD/test_audio_cc ({}).wav".format(j)

        # clean out any residule segments from previous runs
        shutil.rmtree("segments_filtered")
        os.makedirs("segments_filtered")

        # preprocess and transcribe segments
        for j in range(6):
            txtname = "audio_cc{}.txt".format(j)
            preprocess.remove_silence(audio_path=filename, out_directory="segments_filtered")
            print("starting audio segments file {}".format(j))
            f = open("transcription/" + txtname, "w+")
            for i in range(1, len(os.listdir("segments_filtered"))+1):
                audio_path = "segments_filtered/{}audio_segment.wav".format(i)
                preprocess.frequency_filter(audio_path=audio_path, out_path=audio_path, frequency=500)
                preprocess.boost_audio(audio_path=audio_path, boost=10)
                audio = sr.AudioFile(audio_path)
                transcriber = src.transcriber.Transcriber(audio)
                f.write("Transcription for segment " + str(audio_path) + ": " + transcriber.transcribe() + "\n")
                print("segment {} transcribed".format(i))
            f.close()

        # parse text files to get total crime count data frame, and list of tuples in form (address, crime)
        for j in range(6):
            file = "transcription/audio_cc{}".format(j)
            parser = src.parser.Parser(file)
            parser.parse_lines()
            print(parser.get_crime_count())
            print(parser.get_street_crimes())


# run here:
example = Example()
example.example()
