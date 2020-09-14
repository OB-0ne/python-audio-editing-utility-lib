import mido
import numpy as np

class DataManager():
    
    
    def np2MIDI(self, in_filename, out_filename, num = 4, den = 4, clocks = 36, noted32 = 8, AutoTimed = False, AutoTime=120):
            
        max_midi_time = 1000.0

        data = np.load(in_filename)
        mid = mido.MidiFile()
        track = mido.MidiTrack()

        mid.tracks.append(track)
        
        num = 4
        den = 4
        clocks = 36
        noted32 = 8

        track.append(mido.MetaMessage('time_signature', numerator=num, denominator=den, clocks_per_click=clocks, notated_32nd_notes_per_beat=noted32, time=0))
        test=[]

        for msg in data:

            if int(msg[0]+0.5) == 1:
                control = 'note_on'
            else:
                control = 'note_off'
            
            if AutoTimed:
                track.append(mido.Message(control, note=int(msg[1]*127), velocity=int(msg[2]*127), time=AutoTime))
                
            else:
                track.append(mido.Message(control, note=int(msg[1]*127), velocity=int(msg[2]*127), time=int(msg[3]*max_midi_time)))

        if not out_filename[-4] == '.mid':
            out_filename += '.mid'

        mid.save(out_filename)

    def MIDI2np(self, in_filename, out_filname):
        max_midi_time = 1000.0

        def standardizeData(midiData):
            for msg in midiData:
                msg[1] = float(msg[1])/127.0
                msg[2] = float(msg[2])/127.0
                msg[3] = float(msg[3])/max_midi_time
            return midiData


        mid = mido.MidiFile(in_filename)

        i = 0
        mid_out = []

        for i,track in enumerate(mid.tracks):
                
            for msg in track:

                if msg.type == "control_change":
                    #skip for now I guess
                    continue
                elif msg.type == "note_on":
                    mid_out.append([1,msg.note,msg.velocity,msg.time])
                elif msg.type == "note_off":
                    mid_out.append([0,msg.note,msg.velocity,msg.time])

            mid_out = np.array(standardizeData(mid_out))
            np.save(out_filname + str(i),np.array(mid_out))


# MAIN CODE HERE

DM = DataManager()

# example to convert numpy to MIDI
DM.np2MIDI('midi_e7800.npy','MIDI out/track1',AutoTimed=True,AutoTime=180)
DM.np2MIDI('midi_e5150.npy','MIDI out/track2',AutoTimed=True,AutoTime=140)

# example to convert MIDI to numpy
DM.MIDI2np('song.mid','out')

# [OB][NOTE]:
# Autotime can also modify the rhythm, try time signatures