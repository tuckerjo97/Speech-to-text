from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment
from pydub import silence
import noisereduce as nr
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math
import contextlib
import os
import pydub as pd
import soundfile as sf
import re


def remove_silence(audio_path, out_directory):
    """
    Segments audio removing all segments of silence

    :return: A list of lists of times in seconds. Each pair of times indicate start and end time of segments with
    noise
    """
    [fs, x] = aIO.readAudioFile(audio_path)

    segments = aS.silenceRemoval(x, fs, 0.05, 0.02, smoothWindow=1.0, weight=0.3, plot=False)

    dub_audio = AudioSegment.from_wav(audio_path)

    counter = 1
    for segment in segments:
        t1 = segment[0] * 1000
        t2 = segment[1] * 1000
        audio_segment = dub_audio[t1:t2]
        format_name = "{}/{}audio_segment.wav".format(out_directory, counter)
        audio_segment.export(format_name, format="wav")
        counter += 1
    return segments


def noise_reduction(audio_path=None, noisy_part=None, out_path=None):
    """Reduces noise using technique found here: https://github.com/timsainb/noisereduce"""
    rate, data = wavfile.read(audio_path)

    data = data/32768
    noisy_part = noisy_part/32768

    reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=False)

    if outpath:
        wavfile.write(out_path, rate=rate, data=reduced_noise)

    return reduced_noise


def frequency_filter(audio_path, out_path, frequency):
    """Filters out frequencies based on stack overflow answer:
    https://stackoverflow.com/questions/24920346/filtering-a-wav-file-using-python"""
    fname = audio_path
    outname = out_path

    cutOffFrequency = frequency

    def running_mean(x, windowSize):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

    # from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
    def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved=True):

        if sample_width == 1:
            dtype = np.uint8  # unsigned char
        elif sample_width == 2:
            dtype = np.int16  # signed 2-byte short
        else:
            raise ValueError("Only supports 8 and 16 bit audio formats.")

        channels = np.frombuffer(raw_bytes, dtype=dtype)

        if interleaved:
            # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
            channels.shape = (n_frames, n_channels)
            channels = channels.T
        else:
            # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
            channels.shape = (n_channels, n_frames)

        return channels

    with contextlib.closing(wave.open(fname, 'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()

        # Extract Raw Audio from multi-channel Wav File
        signal = spf.readframes(nFrames * nChannels)
        spf.close()
        channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

        # get window size
        # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
        freqRatio = (cutOffFrequency / sampleRate)
        N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)

        # Use moviung average (only on first channel)
        filtered = running_mean(channels[0], N).astype(channels.dtype)

        wav_file = wave.open(outname, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()


def convert_mp3_to_wav(audio_path):
    """writes a new wav file with same name"""
    audio = AudioSegment.from_mp3(audio_path)
    reformatname = audio_path.split(".mp3", maxsplit=1)[0]
    audio.export(reformatname + ".wav", format="wav")


def convert_to_pcm16(audio_path):
    """converts any wav format to PCM-16"""
    audio, rate = sf.read(audio_path)
    sf.write(audio_path, audio, rate, subtype="PCM_16")


def boost_audio(audio_path, boost):
    audio = AudioSegment.from_wav(audio_path)
    audio = audio + boost
    audio.export(audio_path, format="wav")
