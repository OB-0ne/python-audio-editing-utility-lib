Steps to get started
=====================

- Get all the required supporting libraries if you dont have them already. Run the following command:
>  pip3 install -r requirements.txt



Terminal commands for running code
==================================

- Splitting a given audio file in samples by their onset detection
>  python Lib/sampleAudio.py -type onset -au "wav file location" -o "output folder location"



Timber Labeling for wav file
============================

- Make the following structure:
-- test/onset_samples/timber_label_samples

- all onset files should be in the 'onset_sample' folder
- run the following command
>  python lib/timberLabel.py


Timber Labeling for .wav file
=============================

- Open the 'sample2FormCluster.py' file, go to the end and change the file name
- run the following command
>  python lib/sample2FormCluster.py
- outputs should be available in the 'output_samples' folder
- 'cluster_outputs' helps to set if outputs for each clusters is to be generated as wav files
- 'form_outputs' helps to set if outputs for each clustered form is to be generated as wav files
- an audio file of the input with clicks will be generated to identify form