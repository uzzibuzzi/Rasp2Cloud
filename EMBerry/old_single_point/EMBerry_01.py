#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 128 Functions Demonstrated:

    Purpose:
        Read a single data value for each channel in a loop.

    Description:
        This example demonstrates acquiring data using a software timed loop
        to read a single value from each selected channel on each iteration
        of the loop.
"""
from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    chan_list_to_mask, input_mode_to_string, input_range_to_string

#from sys import version_info
from daqhats import mcc152#, OptionFlags, HatIDs, HatError

from datetime import datetime, timedelta
import time

import os
import csv   #this is the import to make csv file creation simple.
import errno

import math

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def main():
    """
    This function is executed automatically when the module is run directly.
    """
    # MCC152
    channel_out = 0
    num_channels_out = mcc152.info().NUM_AO_CHANNELS
    min_v_out = mcc152.info().AO_MIN_RANGE
    max_v_out = mcc152.info().AO_MAX_RANGE
    # Ensure channel is valid.
    if channel_out not in range(num_channels_out):
        error_message = ('Error: Invalid channel output selection - must be '
                         '0 - {}'.format(num_channels_out - 1))
        raise Exception(error_message)
    print("   Channel output: {}\n".format(channel_out))
    # Get an instance of the selected hat device object.
    address_out = select_hat_device(HatIDs.MCC_152)
    print("\nUsing address output {}.\n".format(address_out))
    hat_out = mcc152(address_out)
    # Reset the DIO to defaults (all channels input, pull-up resistors
    # enabled).
    hat_out.dio_reset()
    num_channels_bIOs = hat_out.info().NUM_DIO_CHANNELS
    
    #mcc128
    channels = [0, 1, 2, 3, 4, 5, 6, 7]
    channel_mask = chan_list_to_mask(channels)
    num_channels = len(channels)
    input_mode = AnalogInputMode.SE
    input_range = AnalogInputRange.BIP_10V
    options = OptionFlags.DEFAULT
       
    # other stuff
    sample_interval = 0.02  # In Seconds
    basepath = '/home/pi/EMBerry' 
    mypath = basepath + '/log_data'

    try:
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        hat = mcc128(address)

        print('\nMCC 128 single data value read example')
        print('    Input mode: ', input_mode_to_string(input_mode))
        print('    Input range: ', input_range_to_string(input_range))      
        print('    Channels: ', end='')
        print(', '.join([str(chan) for chan in channels]))
        print('    Options: ', enum_mask_to_string(OptionFlags, options))
        print('    Sample interval:  ' + str(sample_interval) + ' seconds')
                     
        try:
            #input("\nPress 'Enter' to continue")
            print('Switch to start:')
            change_DI = hat_out.dio_input_read_bit(0)
            while hat_out.dio_input_read_bit(0)==change_DI:
                sleep(0.02)
            change_DI = hat_out.dio_input_read_bit(0)
        except (NameError, SyntaxError):
            pass

        print('\nAcquiring data ... Press Ctrl-C to abort or switch')
        
        # file switch:  w =  Write to a file
        # file switch:  w+ = Write to a file, if it doesn't exist create it
        # file switch:  a =  Append to a file
        # file switch:  a+ = Append to a file, if is doesn't exist create it.
        # file switch:  x = will create a file, returns an error if the file exist
    

        # If the scan starts, create a file name based upon current date and time.
        # Retrieve the Current Working Directory and generate the full path 
        # to where to write the collected data as a .csv file.  Open the file 
        # begin writing the data to the file.  When done, close the file.
    
        try:
            if os.path.exists(basepath):
                if not (os.path.exists(mypath)):
                    os.mkdir(mypath)
            else:
                os.mkdir(basepath)
                os.chdir(basepath)
                os.mkdir(mypath)
        except OSError as exc:
            raise
    
        os.chdir(mypath)
        fileDateTime = datetime.strftime(datetime.now(), "%Y_%B_%d_%H%M%S")
        dirpath = os.getcwd()
        fileDateTime = mypath + "/" + fileDateTime + ".csv"
        csvfile = open(fileDateTime, "w+")
        csvwriter = csv.writer(csvfile) 
        myArrayHeader = []
        myArrayHeader.append([]) 
        myArrayHeader[0].append('     Date/Time     ') 

        # Display the header row for the data table.
        print('\n  Time (s)       ', end='')
        for chan in channels: #enumerate(channels)
            print('     Channel', chan, end='')
            myArrayHeader[0].append('   Chan ' + str(chan)) 
        print('')
        csvwriter.writerows(myArrayHeader) # Write the array to file
        csvfile.flush()
        
        t_clk = time.CLOCK_MONOTONIC
        t_0 = time.clock_gettime(t_clk)
        t_last = t_0
        t_disp = 0
        disp_flag = True
        
        try:
            samples_per_channel = 0
            while hat_out.dio_input_read_bit(0)==change_DI:#True:
                
                t_act = time.clock_gettime(t_clk)-t_0 # closer to the read would be better
                
                if (t_act-t_disp)>0.2:
                    disp_flag = True
                    t_disp=t_act
                else:
                    disp_flag = False
                #print('t_act=',t_act,'t_disp=',t_disp,'disp_flag=',disp_flag)
                
                new_index = 0
                myArray=[] #create an empty array
                # Display the updated samples per channel count
                samples_per_channel += 1
                #print('\r{:17}'.format(samples_per_channel), end='')
                if disp_flag:
                    print('\r{:17.5}'.format(t_act), end='')
                
                myArray.append([])  #add a row to the array 
                # Time stamp:
                #timestamp = datetime.strftime(datetime.now(), "%Y %B %d %H:%M:%S.%f")
                
                myArray[new_index].append(t_act)#(timestamp)

                # Read a single value from each selected channel.
                for chan in channels:
                    value = hat.a_in_read(chan, options)
                    if disp_flag:
                        print('{:12.5} V'.format(value), end='')
                    myArray[new_index].append('{:12.5f}'.format(value))

                stdout.flush()
                csvfile = open(fileDateTime, "a")
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerows(myArray) # Write the array to file
                csvfile.flush()

                # Wait the specified interval between reads.
                #sleep(sample_interval)
                while (time.clock_gettime(t_clk)-t_last)<sample_interval:
                    minimum_operation = 0
                t_last = time.clock_gettime(t_clk)
                out_0 = 1.5*math.sin(2*math.pi*t_act)+2            
                hat_out.a_out_write(channel=channel_out,
                                    value = out_0,
                                    options = options)

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)
    
    csvfile.close() 

if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
