import numpy as np
from os.path import join
import librosa as lr
import glob
import soundfile as sf

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

## Setting variables

data_root = 'test/onset_samples/'
load_duration = 0.0464

min_sample_rate = 1024

sr = 44100/2
max_length = sr # ignore samples longer than 7 seconds
fixed_length = sr/4 # trim all samples to 250 milliseconds
n_fft = 1024


## Getting file names to read
## read the samples and get their FFT

files = glob.glob(data_root+'*.wav')

samples = []
label_val = []

for i,file_name in enumerate(files):
    print('working on file... ' + file_name)
    audio, sr = lr.load(file_name, sr = sr, duration=load_duration)

    if audio.shape[0] >= min_sample_rate-10:
        audio_stft = lr.stft(audio, n_fft,win_length=n_fft)
        audio_stft = np.abs(audio_stft)
        audio_stft = lr.amplitude_to_db(audio_stft,ref=np.max)

        #   flatten the audio stft
        audio_stft = audio_stft.reshape((audio_stft.shape[0]*audio_stft.shape[1]))

        samples.append(audio_stft)
        label_val.append(file_name)

samples = np.array(samples)


## Perform a tSNE to get timber similarity analysis

componenets = 2
l_rate = 10
iters = 1500

X = TSNE(n_components=2,learning_rate=l_rate, n_iter=iters).fit_transform(samples)

x_val = [i[0] for i in X]
y_val = [i[1] for i in X]


## Perform a clustering method get labels for 2d tSNE data

n_cluster_tsne2kmeans = 6

X = [[x,y] for x,y in zip(x_val,y_val)]

kmeans = KMeans(n_clusters=n_cluster_tsne2kmeans, random_state=42).fit(X)

cluster_labels = kmeans.labels_


## Combine 10 samples for form clustering
div_variable = 36
n_cluster_form = 5
if len(cluster_labels)%div_variable > 0:
    X_new = np.array(cluster_labels[:-(len(cluster_labels)%div_variable)]).reshape(-1,div_variable)
else:
    X_new = np.array(cluster_labels).reshape(-1,div_variable)
    
kmeans = KMeans(n_clusters=n_cluster_form, random_state=0).fit(X_new)

cluster_labels_new = kmeans.labels_
print(cluster_labels_new)

## throw out wav files of the same cluster

for j in range(n_cluster_tsne2kmeans):
    song = []
    for i, label in enumerate(label_val):
        if cluster_labels[i] == j:
            audio, sr = lr.load(label,sr)
            song.extend(list(audio))
    song = np.array(song)
    sf.write(data_root + 'timber_label_samples/' + str(j)+'_output.wav', song, int(sr))
    print('File saved for cluster ' + str(j))

for j in range(n_cluster_form):
    song = []
    for k, label_form in enumerate(cluster_labels_new):
        if label_form == j:    
            for i, label in enumerate(X_new[k]):
                audio, sr = lr.load(label_val[k*div_variable+i],sr)
                song.extend(list(audio))
    song = np.array(song)
    sf.write(data_root + 'timber_label_samples/form_' + str(j)+'_output.wav', song, int(sr))
    print('File saved for cluster form ' + str(j))