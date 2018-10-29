import os
import matplotlib.pyplot as plt
import pyaudio
import scipy.io.wavfile as wavefile
import math as math
import numpy as np
from matplotlib.mlab import specgram
# source: https://stackoverflow.com/questions/33680633/how-to-change-pyplot-specgram-x-and-y-axis-scaling


def get_specgram_data_from_wav():
    sample_rate, data = wavefile.read(path)

    # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
    res_in_hz = 50

    spectro, freq, t, = specgram(data, Fs=sample_rate, NFFT=math.ceil(sample_rate / res_in_hz))

    return spectro, freq, t


# makes a spectrogram from a wav-file, with the option to include colorbar
def make_specgram_from_wav(make_cbar=True, grid=False):
    # getting the cmap
    cmap = plt.get_cmap("inferno")

    # Sets the color for things going below the scale in the colormap, k = some dark looking color
    cmap.set_under(color="k", alpha=None)

    # reads the wave file and gets the framerate and the frames(info)
    sample_rate, data = wavefile.read(path)

    # figsize is additional parameters, indicating the size of the figure
    # used instead of plt.figure, since we here get a Axesobject .
    fig, axes = plt.subplots(figsize=(20, 12))

    # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
    res_in_hz = 50

    # making the spectrogram, see doc for return values.
    # can also make stereo to mono by saying data[:,0], which takes the first channel
    spectro, freq, t, pic = axes.specgram(data, Fs=sample_rate, cmap=cmap, NFFT=math.ceil(sample_rate/res_in_hz))

    # sets the limits for the y-axis
    axes.set_ylim(0, 17000)

    # if grid is desired, it is made
    if grid:
        # b=True indicates that grid is desired.
        axes.grid(b=True, axis="both", color="w", linewidth=1.2, linestyle="--")

    # sets labels and sizes of labels
    axes.set_xlabel("Time[sec]", fontsize=20)
    axes.set_ylabel("Frequency [Hz]", fontsize=20)
    axes.tick_params(labelsize=20)

    # plots the colorbar
    if make_cbar:
        cbar = fig.colorbar(pic)
        cbar.set_label("Intensity dB", fontsize=20)

    # saves the file in this folder.
    plt.savefig("C:\\Users\\Jacob\\Music\\Samples\\Alle\\Specgrams\\"+name+".png")  # for quick view call this: plt.show()

    # This clears the memory used by the figure.
    # Otherwise memory usage becomes too high if this function is called inside a loop.
    plt.close(fig)


# makes spectrogram for all wav-files in a directory
def make_specgram_for_dir():
    directory = 'C:\\Users\\Jacob\\Music\\Samples\\Alle\\'
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            # splitting in order to get name of file
            args = filename.split(".")
            name_of_file = args[0]
            make_specgram_from_wav(directory+filename, name_of_file)


def make_specgram_from_mic():
    # getting the cmap
    cmap = plt.get_cmap("inferno")

    # Sets the color for things going below the scale in the colormap, k = some dark looking color
    cmap.set_under(color="k", alpha=None)

    # reads the wave file and gets the framerate and the frames(info)
    # sample_rate, data = wavefile.read(path)

    # figsize is additional parameters, indicating the size of the figure
    # used instead of plt.figure, since we here get a Axesobject .
    fig, axes = plt.subplots(figsize=(20, 12))

    # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
    res_in_hz = 50

    #This is standard for pyaudio
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    INPUT_LENGTH = 1  # length of sample to take in sec
    INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_LENGTH)
    TOTALTIME = 15
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

    a_data = []  # the accumulated data used for the spectrogram.

    for x in range(0, TOTALTIME):
        print("Start reading")
        sound_info = stream.read(INPUT_FRAMES_PER_BLOCK)

        data = np.frombuffer(sound_info, dtype=np.int16)

        a_data.extend(data.ravel())

        print("End reading")

        # making the spectrogram, see doc for return values.
        # can also make stereo to mono by saying data[:,0], which takes the first channel
        spectro, freq, t, pic = axes.specgram(data, Fs=RATE, cmap=cmap, NFFT=math.ceil(RATE / res_in_hz))

        # sets the limits for the y-axis
        axes.set_ylim(0, 17000)

        # sets labels and sizes of labels
        axes.set_xlabel("Time[sec]", fontsize=20)
        axes.set_ylabel("Frequency [Hz]", fontsize=20)
        axes.tick_params(labelsize=20)

        # saves the file in this folder.
        plt.savefig(
            "C:\\Users\\Jacob\\Music\\Samples\\Alle\\Specgrams\\"+str(x)+".png")  # for quick view call this: plt.show()

        # This clears the memory used by the figure.
        # Otherwise memory usage becomes too high if this function is called inside a loop.
        plt.close(fig)


if __name__ == "__main__":
    # Full path to the desired wav-file
    path="C:\\Users\\Jacob\\Music\\Samples\\Alle\\Sirene56.wav"
    # name of it.
    name = "Sirene56"
    make_specgram_from_wav(make_cbar=True)
    #make_specgram_from_mic()
    # make_specgram_for_dir()

