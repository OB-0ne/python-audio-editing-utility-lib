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
>  python Lib/timberLabel.py