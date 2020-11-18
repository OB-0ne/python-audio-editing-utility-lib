Steps to get started
=====================

- Get all the required supporting libraries if you dont have them already. Run the following command:
>  pip3 install -r requirements.txt



Terminal commands for running code
==================================

- Splitting a given audio file in samples by their onset detection
>  python Lib/sampleAudio.py -type onset -au "wav file location" -o "output folder location"


Timbre Labeling for .wav file
=============================

- Open the 'sample2FormCluster.py' file, go to the end and change the needed settings
- run the following command
>  python lib/sample2FormCluster.py
- folder should be created with the the files

File created:
- 'cluster_samples' - has all cluster samples
- 'cluster_samples' - has all form combined as samples
- 'audio_beeped' - audio file of the input with clicks will be generated to identify form
- 'form_no_by_seconds' - seconds to identify each form in the original samples (seconds when cick is played)
- 'offset_cluster_tsne' - image of the clustered tSNE

<!-- 
---------OLD----------------
Timbre Labeling for wav file
============================

- Make the following structure:
-- test/onset_samples/timbre_label_samples

- all onset files should be in the 'onset_sample' folder
- run the following command
>  python lib/timbreLabel.py -->