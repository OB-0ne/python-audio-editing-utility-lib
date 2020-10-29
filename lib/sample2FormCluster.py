# Import needed libraries
import librosa as lr
import numpy as np
import soundfile as sf

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

def getOnsetSamplesWithTime(audio_filename, sr = 22050, min_sample_length=1024, onset_hop_length = 1024):
    
    # Read the sample
    audio, sr = lr.load(audio_filename, sr=sr)

    # get onset frames and time in seconds
    onset_frames = lr.onset.onset_detect(audio, sr=sr, hop_length=onset_hop_length)

    # get the onsets into small samples for analysis
    onset_samples = []
    onset_time = []

    # calculating the chunk samples
    frame_before = 1 
    frame_after = int(sr/(10*onset_hop_length))
    chunk = ((frame_before + frame_after) - 1 ) * onset_hop_length

    for i in range(len(onset_frames)-1):

        #make an empty feature matrix
        feature_matrix = np.zeros((chunk), dtype='float32')

        #get the start and end point for the sample
        start = (onset_frames[i] - frame_before) * onset_hop_length
        end = (onset_frames[i+1] - frame_before - 1) * onset_hop_length

        if end-start >= min_sample_length:
            feature_matrix = audio[start:start+min_sample_length]

            # append to the actual sample matrix
            onset_samples.append(sample2timeAnalysis(feature_matrix, n_fft=min_sample_length))
            onset_time.append(start)

    # convert samples to array and time to seconds
    onset_samples = np.array(onset_samples)
    onset_time_sampleno = np.array(onset_time)

    # both return variables are a arrays of np arrays
    return audio, onset_samples, onset_time_sampleno

def sample2timeAnalysis(sample, n_fft=1024):

    # do stft band get timbre analysis
    audio_stft = lr.stft(sample, n_fft,win_length=n_fft)
    audio_stft = np.abs(audio_stft)
    audio_stft = lr.amplitude_to_db(audio_stft,ref=np.max)

    #   flatten the audio stft
    audio_stft = audio_stft.reshape((audio_stft.shape[0]*audio_stft.shape[1]))

    return audio_stft

def samples2tSNE(features, componenets = 2, l_rate = 10, iters = 1500):

    tSNE_points = TSNE(n_components=componenets,learning_rate=l_rate, n_iter=iters).fit_transform(features)

    return tSNE_points

def samples2Cluster(features, n_clusters):

    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(features)

    return kmeans.labels_

def formWithTime(form_labels, form_time):

    # convert the sample time to seconds
    form_time = list(lr.samples_to_time(form_time))

    # print the time in seconds with form label
    for time, form_label in zip(form_time,form_labels):
        print(round(time,2)," --- ",form_label)

    return -1

def saveCluster2Wav(audio, time, labels, sr=22050, output_filename="_output"):

    # add the total time at the end of array for not missing the last samples
    time = np.append(time,len(audio))

    # loop on each label to make their output samples
    for j in range(max(labels)+1):
        song = []
        for i, label in enumerate(labels):
            if label == j:
                song.extend(list(audio[time[i]:time[i+1]]))
        song = np.array(song)
        sf.write('output_samples/' + str(j) + output_filename + '.wav', song, int(sr))

def saveAudioWithFormBeeps(audio, time, sr=22050):

    # generating a track with clicks at the start of forms
    clicks = lr.clicks(times=lr.samples_to_time(time), length=len(audio))

    # adsd the clicks to original audio and save it
    sf.write('output_samples/' + 'audio_beeped.wav', audio+clicks, int(sr))

def sample2FormCluster(audio_filename, cluster_outputs=False, form_outputs=False):

    # set needed variables
    sr = 22050                  # CHANGE for sampliung wave at a different rate
    timbre_seconds = 0.2        # CHANGE for timbre analysis
    form_bundle = 12            # CHANGE for form analysis bundling
    
    # calculate the samples needed for timbre analysis
    n_fft = int(sr * timbre_seconds)

    # read audio, disect it on onsets and get timbre analysis features
    audio, samples, sample_time = getOnsetSamplesWithTime(audio_filename, sr=sr, min_sample_length=n_fft)

    # conpute a t-SNE on the features made
    features = samples2tSNE(samples)

    # cluster the t-SNE points to get similar timbre samples
    sample_labels = samples2Cluster(features, 12)
    
    # form larger bundled samples, and cluster them to recognize similar forms
    form_input = np.array(sample_labels[:-(len(sample_labels)%form_bundle)]).reshape(-1,form_bundle)
    form_start_time = [sample_time[i] for i in range(len(sample_time)) if i % form_bundle == 0][:-1]
    form_labels = samples2Cluster(form_input, 3)

    # get the form with their corresponding time
    formWithTime(form_labels, form_start_time)

    # throw out 
    if cluster_outputs:
        saveCluster2Wav(audio, sample_time, sample_labels, sr=sr)
    if form_outputs:
        saveCluster2Wav(audio, form_start_time, form_labels, sr=sr, output_filename='_form_output')

    #saves the same audio wuith clicks in them
    saveAudioWithFormBeeps(audio, form_start_time, sr=sr)

filename = 'test/test_gov.wav'
sample2FormCluster(filename, cluster_outputs=True, form_outputs=True)