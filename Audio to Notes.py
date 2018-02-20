############################################################################
#																		   #
#			Musical Note Identification							   #
#																		   #
############################################################################

import numpy as np
import wave
import struct

#Teams can add other helper functions
#which can be added here


sampling_freq = 44100	# Sampling frequency of audio signal
c=2205
notes=[]
notes=(['C6',1018 ,1127],['D6',1128 ,1281] ,['E6',1282 ,1357], ['F6',1358 ,1523],['G6',1524, 1710], ['A6',1711 ,1919], ['B6',1920 ,2034], ['C7',2035 ,2283], ['D7',2284 ,2562], ['E7',2563 ,2715],['F7',2716 ,3047], ['G7',3048 ,3420], ['A7',3421 ,3839], ['B7',3840 ,4068], ['C8',4069 ,4566], ['D8',4567 ,5125], ['E8',5126 ,5430], ['F8',5431 ,6095] ,['G8',6096 ,6841] ,['A8',6842,7679], ['B8',7680 ,7910],['nan',0,50])
def play(sound_file):
    '''
    sound_file-- a single test audio_file as input argument
    
    #add your code here

    '''
    sf=sound_file
    swidth = sf.getsampwidth()
    RATE = sf.getframerate()
    window = np.blackman(c)

    fre=[]
    data = sf.readframes(c)
    while len(data) == c*swidth:
    
    
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    
        fftData=abs(np.fft.rfft(indata))**2
        m = fftData[1:].argmax() + 1
        if m != len(fftData)-1:
            if(any(fftData[m-1:m+2:])>0):
             y0,y1,y2 = np.log(fftData[m-1:m+2:])
             x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        
            freq = (m+x1)*RATE/c
            fre.append(freq)
            
        else:
            freq = m*RATE/c
            fre.append(freq)
            
   
        data = sf.readframes(c)
    
        
    b=[]
    for i in range(0,len(fre)):
     try:   
      for row in notes:
         if((fre[i]>row[1])&(fre[i]<row[2])):
          b.append(row[0])
     except:
         continue

    Identified_Notes = []
    q= None
    for e in b:
        if e != q:
            Identified_Notes.append(e)
            q = e

    for o in Identified_Notes:
        if o=='nan':
            Identified_Notes.remove('nan')
    return Identified_Notes

############################## Read Audio File #############################

if __name__ == "__main__":
    #code for checking output for single audio file
    sound_file = wave.open('Audio_files/Audio_1.wav', 'r')
    Identified_Notes = play(sound_file)
    print "Notes = ", Identified_Notes

    #code for checking output for all images
    Identified_Notes_list = []
    for file_number in range(1,6):
        file_name = "Audio_files/Audio_"+str(file_number)+".wav"
        sound_file = wave.open(file_name)
        Identified_Notes = play(sound_file)
        Identified_Notes_list.append(Identified_Notes)
        print Identified_Notes
   


