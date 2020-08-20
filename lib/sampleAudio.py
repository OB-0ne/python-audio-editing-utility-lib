import pandas as pd
import numpy as np
import librosa as lr
import soundfile as sf
import os
import argparse
import sys


def byOnsets(input_file, output_folder, sample_name):

    sr = int(44100/2)
    onset_hop_length = 1024
    frame_before = 1 
    frame_after = int(sr/(10*onset_hop_length))

    file_loc = input_file

    #specifics for the audio extraction
    sr = int(44100/2)
    onset_hop_length = 1024
    frame_before = 1 

    # calculating the chunk samples
    chunk = ((frame_before + frame_after) - 1 ) * onset_hop_length

    #read the audio in librosa
    audio, sr = lr.load(file_loc, sr=sr)

    #get onset frames
    onset_frames = lr.onset.onset_detect(audio, sr=sr,hop_length=onset_hop_length)

    for i in range(len(onset_frames)-1):

        #make an empty feature matrix
        feature_matrix = np.zeros((chunk), dtype='float32')

        #get the start and end point for the sample
        start = (onset_frames[i] - frame_before) * onset_hop_length
        end = (onset_frames[i+1] - frame_before - 1) * onset_hop_length

        feature_matrix = audio[start:end]

        #append to the actual matrix
        # make a folder named "output_data" so all samples are generated in there
        song_name = output_folder + sample_name + str(i) + ".wav"
        sf.write(song_name,feature_matrix,sr)

#Initialize the parser
parser = argparse.ArgumentParser(description="Sample an audio file by various methods.")

#Add parser arguments
parser.add_argument("-type", action="store", dest="sample_by", required=True, help="Sampling method")
parser.add_argument("-au", action="store", dest="audio_sample", required=True, help="Input Audio sample file name")
parser.add_argument("-o", action="store", dest="output_dir", required=True, help="Output folder name/path")
parser.add_argument("-outname", action="store", dest="out_name", nargs='?', default="sample_", help="Output sample name, DEFAULT='sample_n.wav'")

arguments = parser.parse_args()

if arguments.sample_by == "onset":
    
    #Check if file and folder exist
    if not os.path.exists(arguments.audio_sample):
        sys.exit("The audio file - '" + arguments.audio_sample + "' deosn't exist. Try Again.")
    if not os.path.isdir(arguments.output_dir):
        sys.exit("The output folder - '" + arguments.output_dir + "' deosn't exist. Try Again.")

    #add a seperator to the path if it doesn't exist
    arguments.output_dir = os.path.join(arguments.output_dir, '')

    #call the function
    byOnsets(arguments.audio_sample,arguments.output_dir,arguments.out_name)

else:
    sys.exit("Selected type '" + arguments.sample_by + "' invalid. Try Again.")