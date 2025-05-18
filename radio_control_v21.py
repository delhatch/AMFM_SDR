# v4 adds eeprom
# v5 adds volume & tuning control
# v6 adds IF Bandwidth control
# v9 works well. Added IF filter slope and Blend frequency
# v10 adds tuning hysteresis
# v12 adds scroll speed and fine tuning
# v13 adds a main state machine
# v14 adds station memory (Mem1 only)
# v15 adds more memory buttons
from xmlrpc.client import ServerProxy
from smbus2 import SMBus
import struct
import random
import time
from gpiozero import MCP3008
from gpiozero import Button

#--------------------
# psutil is a Raspberry Pi (only) library for reading CPU stats.
import psutil
import sys

mem = []
amfmSwitch = Button(17)
memSet = Button(27)
gpio_pins = [22, 23, 24, 25, 5, 6, 13, 16]
for pin in gpio_pins:
    mem.append(Button(pin))

memSize = 16  # How many bytes are stored/recalled when mem button pressed.
pressedButton = 0

junk16 = 16
minFM = 87.5
maxFM = 107.9
minAM = 0.53
maxAM = 1.7
goUp = True
deltaFM = maxFM - minFM
deltaAM = maxAM - minAM
minFMBW = 50000
maxFMBW = 300000
minAMBW = 1000
maxAMBW = 15000
deltaFMBW = 0.025  # Ignore changes in FM IF BW until change is > 3%
deltaAMBW = 0.03  # Ignore changes in AM IF BW until change is > 3%
volGain = 0.0
oldVolGaindb = 0
volMaxCut = 40
currentAMFMSwitch = amfmSwitch.is_pressed
oldAMFMSwitch = amfmSwitch.is_pressed
isAM = False
AMTrimFactor = 250
FMTrimFactor = 1500
freqCorrFactor = 20

xmlrpc_control_client = ServerProxy('http://'+'localhost'+':8080')
delay = 0.1

ebus = SMBus(1)
eAddr = 0x50

# Configure the MCP3008 ADC
tunePot = MCP3008(0)
bwPot = MCP3008(1)
IFslopePot = MCP3008(2)
blendPot = MCP3008(3)
volumePot = MCP3008(4)
freqTrimPot = MCP3008(5)
scrollPot = MCP3008(6)

#----  Functions  -----
def doVolume():
    global oldVolGaindb
    volumePot = MCP3008(4)
    tempVolume = volumePot.value
    time.sleep(0.01)
    tempVol2 = volumePot.value
    tempVolume = (tempVolume+tempVol2)/2.0
    if( tempVolume < 0.03 ): # If volume pot all way down (or close), mute.
        newVolume = 0.0
        newVolGaindb = 100   # remember mute as "100" dB cut.
    else:
        volGaindb = ( 1 - tempVolume ) * volMaxCut # Calc dB to cut, 0 to 30.
        newVolGaindb = round(volGaindb)   # Round cut to nearest 1 dB
        volGain = 1 / (10 ** (newVolGaindb/20)) # What multiplier = X db cut?
        newVolume = volGain
    if( abs(newVolGaindb - oldVolGaindb) > 1.3 ): # Send if vol changes by > 1.3 dB.
        #print(newVolGaindb)
        #print("Vol = ", newVolume)
        oldVolGaindb = newVolGaindb
        xmlrpc_control_client.set_volume(newVolume)
        time.sleep(0.05)
    return

def doForceVolume():
    global oldVolGaindb
    volumePot = MCP3008(4)
    tempVolume = volumePot.value
    time.sleep(0.01)
    tempVol2 = volumePot.value
    tempVolume = (tempVolume+tempVol2)/2.0
    if( tempVolume < 0.03 ): # If volume pot all way down (or close), mute.
        newVolume = 0.0
        newVolGaindb = 100   # remember mute as "100" dB cut.
    else:
        volGaindb = ( 1 - tempVolume ) * volMaxCut # Calc dB to cut, 0 to 30.
        newVolGaindb = round(volGaindb)   # Round cut to nearest 1 dB
        volGain = 1 / (10 ** (newVolGaindb/20)) # What multiplier = X db cut?
        newVolume = volGain
    #oldVolGaindb = newVolGaindb
    xmlrpc_control_client.set_volume(newVolume)
    time.sleep(0.05)
    return

def gotoAM( thisVolume ):
    vol = 0
    #print("About to set volume to 0.\n")
    xmlrpc_control_client.set_volume(vol)
    time.sleep(0.05)
    #am_ifbw = 5000
    #xmlrpc_control_client.set_am_ifbw(am_ifbw)
    #time.sleep(0.1)
    #cent_freq = 1000e3
    #xmlrpc_control_client.set_cent_freq(cent_freq)
    #time.sleep(0.1)
    AM1 = 1   # 1 = is AM
    #print("About to set AM1\n")
    xmlrpc_control_client.set_AM1(AM1)
    time.sleep(0.05)
    #print("About to restore the volume.\n")
    doForceVolume()
    #xmlrpc_control_client.set_volume(thisVolume)
    #time.sleep(0.05)
    #FM1 = 0
    #xmlrpc_control_client.set_FM1(FM1)
    #print("Now in AM mode\n")
    return AM1

def gotoFM(thisVolume):
    vol = 0
    xmlrpc_control_client.set_volume(vol)
    time.sleep(0.05)
    #fm_ifbw = 200e3
    #xmlrpc_control_client.set_fm_ifbw(fm_ifbw)
    #time.sleep(delay)
    #cent_freq = 98.1e6
    #xmlrpc_control_client.set_cent_freq(cent_freq)
    #time.sleep(0.1)
    #FM1 = 1
    #xmlrpc_control_client.set_FM1(FM1)
    AM1 = 0   # 0: Not AM = so FM
    xmlrpc_control_client.set_AM1(AM1)
    time.sleep(0.05)
    doForceVolume()
    #xmlrpc_control_client.set_volume(thisVolume)
    #time.sleep(0.05)
    #print("Now in FM mode\n")
    return AM1

def convertPot2AM( pot, old ): # If new AM tuning freq < threshold, return old.
    # old is current tuning frequency, in MHz.
    # All math, and all values, are in MHz.
    thresh = 0.007
    newTuner = deltaAM * pot
    newTuner = newTuner + minAM # newTuner in MHz. Ready for threshold detection
    #print("Raw tune = ", newTuner)
    if( abs(newTuner-old) > thresh ):
        newTuner = round(newTuner/0.01) * 0.01 # Rounds to nearest 10 kHz.
    else:
        newTuner = old
    return newTuner
    
def convertPot2FM( pot, old ):
    thresh = 0.14
    newTuner = deltaFM * pot
    newTuner = newTuner + minFM
    #print("Raw tune = ", newTuner)
    if( abs(newTuner-old) > thresh ):
        newTuner = round(newTuner/0.2) * 0.2 # Rounds to nearest 0.2 MHz.
        newTuner = newTuner - 0.1
    else:
        newTuner = old
    return newTuner

#------  End of functions ------------

# Initial Volume level
tempVolume = volumePot.value
if( tempVolume < 0.03 ):  # If volume pot all the way down (or close), mute
    oldVolume = 0.0
    oldVolGaindb = 100   # remember mute as "100" dB cut.
else:
    volGaindb = ( 1 - tempVolume ) * volMaxCut # Calc dB to cut, 0 to 30.
    oldVolGaindb = round(volGaindb)   # Round cut to nearest 1 dB
    volGain = 1 / (10 ** (oldVolGaindb/20)) # What multiplier = X db cut?
    oldVolume = volGain
#print(oldVolGaindb)
#print(oldVolume)
xmlrpc_control_client.set_volume(oldVolume)
time.sleep(0.05)

# Initial Change to AM or FM as demanded by the switch setting
if( amfmSwitch.is_pressed ):   # Set FM mode
    print("Switch set to FM")
    isAM = gotoFM(oldVolume)
else:   # To AM
    print("Switch set to AM")
    isAM = gotoAM(oldVolume)
print("isAM = ", isAM)

# Initial Tuning  -------------------------------
tempTune = tunePot.value
oldTune = deltaFM * tempTune
oldTune = oldTune + minFM
oldTune = round(oldTune/0.2) * 0.2
oldTune = oldTune - 0.1
print(oldTune)
freq = oldTune * 1e6
xmlrpc_control_client.set_cent_freq(int(freq))
time.sleep(0.05)
xmlrpc_control_client.set_disp_freq(int(freq)) # Display the tuned frequency
time.sleep(0.05)
# Initial BW  ------------------------------------
tempBW = bwPot.value * 300  # Max BW = 300 kHz
oldBW = int(round( tempBW * 1000 ))
if( oldBW < minFMBW ):
    oldBW = minFMBW
if( oldBW > maxFMBW ):
    oldBW = maxFMBW
fm_ifbw = int( oldBW )
xmlrpc_control_client.set_fm_ifbw(fm_ifbw)
time.sleep(0.05)
#Initial Blend frequency -------------------------
tempBlend = blendPot.value
oldBlend = int(10**((1.8 * tempBlend)+2.4))
print(oldBlend)
xmlrpc_control_client.set_blend_freq(oldBlend)
time.sleep(0.05)
#Initial IF slope width, in Hz -------------------
tempSlope = IFslopePot.value
oldAMSlope = int(10**((1.3 * tempSlope)+2.4))
print("AM IF transition width = ", oldAMSlope)
oldFMSlope = int(10**(tempSlope + 3.7))
print("FM IF transition width = ", oldFMSlope)
#Initial Scroll Speed (Waterfall scroll speed) ---
tempScroll = scrollPot.value
if( tempScroll < 0.01 ):
    tempScroll = 0.01
oldScroll = 10**((1.7 * tempScroll)+0.3)
oldScroll = 1 / oldScroll
print("Scroll speed = ", oldScroll)
xmlrpc_control_client.set_scroll_speed(oldScroll)
time.sleep(0.05)
# Initial fine tuning amount --------------
#freqTrim = freqTrimPot.value
#old_freq_correct = (0.5 - freqTrim) * freqCorrFactor
old_freq_correct = 0.0
xmlrpc_control_client.set_freq_correct( int(old_freq_correct) )
time.sleep(0.05)
##oldAMfine = (0.5 - freqTrim)*AMTrimFactor
##print("AM freqTrim = ", oldAMfine )
##oldFMfine = (0.5 - freqTrim)*FMTrimFactor
##print("FM freqTrim = ", oldFMfine )

def doVolume():
    global oldVolGaindb
    volumePot = MCP3008(4)
    tempVolume = volumePot.value
    time.sleep(0.01)
    tempVol2 = volumePot.value
    tempVolume = (tempVolume+tempVol2)/2.0
    if( tempVolume < 0.03 ): # If volume pot all way down (or close), mute.
        newVolume = 0.0
        newVolGaindb = 100   # remember mute as "100" dB cut.
    else:
        volGaindb = ( 1 - tempVolume ) * volMaxCut # Calc dB to cut, 0 to 30.
        newVolGaindb = round(volGaindb)   # Round cut to nearest 1 dB
        volGain = 1 / (10 ** (newVolGaindb/20)) # What multiplier = X db cut?
        newVolume = volGain
    if( abs(newVolGaindb - oldVolGaindb) > 1.3 ): # Send if vol changes by > 1.3 dB.
        #print(newVolGaindb)
        #print("Vol = ", newVolume)
        oldVolGaindb = newVolGaindb
        xmlrpc_control_client.set_volume(newVolume)
        time.sleep(0.05)
    return
#----------------------------------------------
def doTuning():
    global oldAMfine, oldFMfine, oldTune
    returnMainFreq = int(oldTune * 1e6)
    
    tempTune1 = tunePot.value
    time.sleep(0.02)
    tempTune2 = tunePot.value
    time.sleep(0.02)
    tempTune3 = tunePot.value
    time.sleep(0.02)
    tempTune4 = tunePot.value
    tempTune = (tempTune1+tempTune2+tempTune3+tempTune4)/4.0
    
    if( isAM == 1 ):
        newTune = convertPot2AM( tempTune, oldTune ) # newTune in MHz
    else:
        newTune = convertPot2FM( tempTune, oldTune )
    
    if( newTune != oldTune ):
        # print("Tuning to : ", int(newTune*1e6)/(1e6), " MHz")
        oldTune = newTune
        returnMainFreq = int(oldTune * 1e6)
        freq = newTune * 1e6
        xmlrpc_control_client.set_disp_freq(int(freq)) # Show prior to trimming
        time.sleep(0.05)
        try:
            xmlrpc_control_client.set_cent_freq(int(freq)) # Actual tuner freq.
        except:
            print("Tuning Retry 1")
            time.sleep(0.5)
            try:
                xmlrpc_control_client.set_cent_freq(int(freq))
            except:
                print("Tuning Retry 2")
                time.sleep(0.5)
                xmlrpc_control_client.set_cent_freq(int(freq))
        # When tuning has been touched, force IFBW and IFSlope to reset to panel
        doIFBW( True )
        
    return returnMainFreq
#----------------------------------------------
def doTestTuning():
    # Just scroll up and down the dial over and over
    global oldAMfine, oldFMfine, oldTune
    global goUp
    returnMainFreq = int(oldTune * 1e6)

    #print("goUp = ", goUp)
    if( isAM == 1 ):
        #newTune = convertPot2AM( tempTune, oldTune ) # newTune in MHz
        newTune = oldTune + 0.01
    else:
        #print("oldTune = ", oldTune)
        #newTune = convertPot2FM( tempTune, oldTune )
        if( goUp ):
            newTune = oldTune + 0.2
            #print("newTune = ", newTune)
            if (newTune >= maxFM ):
                goUp = False
                newTune = maxFM
            else:
                pass
        else:
            newTune = oldTune - 0.2
            if (newTune < minFM ):
                goUp = True
                newTune = minFM
            else:
                pass
    
    if( newTune != oldTune ):
        # print("Tuning to : ", int(newTune*1e6)/(1e6), " MHz")
        oldTune = newTune
        returnMainFreq = int(oldTune * 1e6)
        freq = newTune * 1e6
        xmlrpc_control_client.set_disp_freq(int(freq)) # Show prior to trimming
        time.sleep(0.05)
        try:
            xmlrpc_control_client.set_cent_freq(int(freq)) # Actual tuner freq.
        except:
            print("Tuning Retry 1")
            time.sleep(0.5)
            try:
                xmlrpc_control_client.set_cent_freq(int(freq))
            except:
                print("Tuning Retry 2")
                time.sleep(0.5)
                xmlrpc_control_client.set_cent_freq(int(freq))
        # When tuning has been touched, force IFBW and IFSlope to reset to panel
        doIFBW( True )
        
    return returnMainFreq
#----------------------------------------------
def doFreqCorrect():
    global AMTrimFactor, FMTrimFactor, old_freq_correct, freqCorrFactor
    # Now read the fine trim pot
    freqTrim = freqTrimPot.value
    time.sleep(0.01)
    freqTrim2 = freqTrimPot.value
    freqTrim = (freqTrim+freqTrim2)/2.0
    new_freq_correct = (0.5 - freqTrim) * freqCorrFactor
    if( int(new_freq_correct) != int(old_freq_correct) ):
        xmlrpc_control_client.set_freq_correct( int(new_freq_correct) )
        time.sleep(0.05)
        old_freq_correct = new_freq_correct
        print("freq correct = ", int(new_freq_correct) )
    #newAMfine = (0.5 - freqTrim)*AMTrimFactor
    #print("AM freqTrim = ", newAMfine)
    #newFMfine = (0.5 - freqTrim)*FMTrimFactor
    #print("FM freqTrim = ", newFMfine)
    '''
    if( isAM == 1 ):
        if( abs(newAMfine - oldAMfine) > 8 ): # Send if changes by > 2 Hz
            oldAMfine = newAMfine
            print("AM freqTrim = ", newAMfine)
            freq = (oldTune * 1e6) + newAMfine
            xmlrpc_control_client.set_cent_freq(int(freq)) # Actual tuner freq.
    else:
        #print( abs(newFMfine - oldFMfine)/oldFMfine )
        if( abs(newFMfine - oldFMfine) > 15 ): # Send if changes by > 15 Hz.
            oldFMfine = newFMfine
            print("FM freqTrim = ", newFMfine)
            freq = (oldTune * 1e6) + newFMfine
            xmlrpc_control_client.set_cent_freq(int(freq)) # Actual tuner freq.
    '''
#----------------------------------------------
def doIFBW( forceUpdate ):
    global oldBW
    
    tempBW = bwPot.value
    if( isAM == 1 ):
        tempBW *= 15.0     # Max AM BW = 15 kHz
        newBW = int( round( tempBW * 1000 ) )
        if( newBW < minAMBW ):
            newBW = minAMBW
        if( newBW > maxAMBW ):
            newBW = maxAMBW
        if( ((abs(newBW - oldBW)/oldBW) > deltaAMBW) or forceUpdate ): # Send if changes by > 5%.
            oldBW = int( newBW )
            am_ifbw = int( newBW )
            #print( "AM IF bandwidth = ", am_ifbw )
            xmlrpc_control_client.set_am_ifbw(am_ifbw)
            time.sleep(0.05)
    else:
        tempBW *= 300.00    # Max FM BW = 300 kHz
        newBW = int( round( tempBW * 1000 ) )
        if( newBW < minFMBW ):
            newBW = minFMBW
        if( newBW > maxFMBW ):
            newBW = maxFMBW
        if( ((abs(newBW - oldBW)/oldBW) > deltaFMBW) or forceUpdate ): # Send if changes by > 5%.
            oldBW = int( newBW )
            fm_ifbw = int( newBW )
            #print( "FM IF bandwidth = ", fm_ifbw )
            xmlrpc_control_client.set_fm_ifbw(fm_ifbw)
            time.sleep(0.05)
    return
#----------------------------------------------
def doBlending():
    global oldBlend
    if( isAM == 0 ):  # Adjust the stereo blending only in FM mode, duh.
        tempBlend = blendPot.value
        time.sleep(0.01)
        tempBlend2 = blendPot.value
        tempBlend = (tempBlend + tempBlend2) / 2
        newBlend = int(10**((1.8 * tempBlend)+2.4))
        if( (abs(newBlend - oldBlend)/oldBlend) > 0.05 ): # Send if changes by > 5%.
            oldBlend = int( newBlend )
            print("FM Blend frequency = ", oldBlend)
            xmlrpc_control_client.set_blend_freq(newBlend)
            time.sleep(0.05)
    return
#------------------------------------------
def doIFSlope( forceUpdate ):
    global oldAMSlope, oldFMSlope
    
    tempSlope = IFslopePot.value
    time.sleep(0.01)
    tempSlope2 = IFslopePot.value
    tempSlope = (tempSlope + tempSlope2) / 2
    if( isAM == 1 ):
        newAMSlope = int(10**((1.3 * tempSlope)+2.4))
        if( (abs(newAMSlope - oldAMSlope)/oldAMSlope) > 0.05 ): # Send if changes by > 5%.
            oldAMSlope = int( newAMSlope )
            print("AM IF transition width = ", newAMSlope)
            xmlrpc_control_client.set_am_xition_width(newAMSlope)
            time.sleep(0.05)
    else:
        newFMSlope = int(10**(tempSlope + 3.7))
        if( (abs(newFMSlope - oldFMSlope)/oldFMSlope) > 0.05 ): # Send if changes by > 5%.
            oldFMSlope = int( newFMSlope )
            print("FM IF transition width = ", newFMSlope)
            xmlrpc_control_client.set_fm_xition_width(newFMSlope)
            time.sleep(0.05)
    return
#-----------------------------------------
def setScrollSpeed():
    global oldScroll
    
    tempScroll = scrollPot.value
    time.sleep(0.01)
    tempScroll2 = scrollPot.value
    tempScroll = 1-((tempScroll + tempScroll2) / 2)
    if( tempScroll < 0.01 ):
        tempScroll = 0.01
    newScroll = 10**((1.7 * tempScroll)+0.3)
    newScroll = 1 / newScroll
    if( (abs(newScroll - oldScroll)/oldScroll) > 0.05 ): # Send if changes by > 5%.
            oldScroll = newScroll
            print("Scroll speed = ", newScroll)
            xmlrpc_control_client.set_scroll_speed(newScroll)
            time.sleep(0.05)
#-----------------------------------------
def store2button( which ):
    global memSize, oldTune, oldBW, oldFMSlope, eAddr
    if( which >= 5 ):
        which += 1
    # Store frequency into address 0x00
    storeAddr = (int(which)) * (memSize)  # Button one stores to addr 0x00, 2->12,etc.
    print("Storing button ", which)
    data_block = list( struct.pack('>fIII', oldTune, oldBW, oldFMSlope, junk16 ))
    print("oldTune = ", oldTune )
    print("oldBW = ", oldBW )
    print("oldFMSlope = ", oldFMSlope )
    data_block.insert(0, storeAddr)  # First byte is now the EEPROM storing addr.
    #print("data_block = ", data_block)
    ebus.write_i2c_block_data( eAddr,0,data_block )
    time.sleep(0.1)
#-----------------------------------------
def recallButton( which ):
    global memSize, eAddr
    if( which >= 5 ):
        which += 1
    readAddr = (int(which)) * (memSize)
    print("Recalling memory ", which)
    #print(" from address ", readAddr)
    ebus.write_i2c_block_data(eAddr,0,[readAddr])  # Start reading at ROM addr
    time.sleep(0.1)
    read_data = ebus.read_i2c_block_data( eAddr, 0, memSize )
    time.sleep(0.1)
    read_freq, readBW, readIFSlope, junk16 = struct.unpack('>fIII', bytes(read_data))
    print("Tune read_freq = ", read_freq )
    #print("readBW = ", readBW )
    #print("readIFSlope = ", readIFSlope )
    xmlrpc_control_client.set_cent_freq(int(read_freq * 1e6))
    time.sleep(0.05)
    read_freq = round(read_freq/0.1) * 0.1 # Rounds to nearest 0.2 MHz.
    #read_freq = read_freq - 0.1
    print("Display read_freq = ", read_freq )
    xmlrpc_control_client.set_disp_freq(int(read_freq * 1e6)) # Display the tuned frequency
    time.sleep(0.05)
    fm_ifbw = int( readBW )
    print( "Recalled FM IF bandwidth = ", fm_ifbw )
    xmlrpc_control_client.set_fm_ifbw(fm_ifbw)
    time.sleep(0.05)
    print("Recalled FM IF transition width = ", readIFSlope)
    xmlrpc_control_client.set_fm_xition_width(readIFSlope)
    time.sleep(0.05)
#----------------------------------------
def get_button_pressed():
    # Returns a value 0 to 7, or 99.
    for i in range(8):
        if( mem[i].is_pressed ):
            return i
    return 99
#-----------------------------------------
# MAIN STATE MACHINE
#-----------------------------------------
state = "run"
tunedFreq = 0
while( True ):
    time.sleep(0.1)
    if( memSet.is_pressed ):
        print("memSet pressed")
    """
    if( mem1.is_pressed ):
        print("mem1 pressed")
    """
    
    #---------------------------------------------
    currentAMFMSwitch = amfmSwitch.is_pressed
    if( currentAMFMSwitch != oldAMFMSwitch ):
        oldAMFMSwitch = currentAMFMSwitch
        if( currentAMFMSwitch ):   # Set FM mode
            isAM = gotoFM(oldVolume)
        else:   # To AM
            isAM = gotoAM(oldVolume)
        time.sleep(0.15)
    #----------------------------------------
    if( state == "run" ):
        doVolume()
        tunedFreq = doTuning()  # tuned frequency in integer Hz.
        #tunedFreq = doTestTuning()
        #doFreqCorrect()
        doIFBW( False )
        doIFSlope( False )
        doBlending()
        setScrollSpeed()
        if( memSet.is_pressed ):
            print("memSet pressed")
            state = "memSet"

        pressedButton = get_button_pressed()
        #print(pressedButton)
        if( pressedButton != 99 ):
            print("Button ",pressedButton," was pressed")
        if( pressedButton != 99 ):
            state = "recall"
        """
        if( mem1.is_pressed ):
            print("Recalling button 1")
            state = "recall"
        """
    elif( state == "memSet"):
        pressedButton = get_button_pressed()
        if( pressedButton != 99 ):
            store2button( pressedButton + 1 )
        """
        if( mem1.is_pressed ):
            store2button( 1 )
        """
        if( not memSet.is_pressed ):
            print("memSet not pressed")
            state = "run"
    elif( state == "recall" ):
        print("In recall")
        recallButton( pressedButton + 1)
        """
        if( mem1.is_pressed ):
            recallButton( 1 )
        """
        state = "run"

