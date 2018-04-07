#!/usr/bin/env python

# ASuMa, Mar 2018
# Read data from files, calculate and plot Parson's coefficient
# See main() documentation below for usage details

import platform
import getopt, sys
import matplotlib.pyplot as plt
import numpy as np

def version():
    """
        Prints Python version used
    """
    print("Code writen for Python3.6.4. You're using python version:")
    print(platform.python_version())

def Load_File(filename):
    """
        Loads a data file
    """
    with open(filename) as file:
        data = file.readlines()
    return data

def Increase_Dictionary(dictio, data):
    """
        Add the fmi value in correct word-pair data to the given dictionary
    """
    for line in data:
        split = line.split()
        name = split[0] + " " + split[1]
        fmi = float(split[2])
        dictio.setdefault(name, []).append(fmi)
    return dictio

def Plot_Scatter(dictio, savefile):
    """
        Calculates Pearson's coefficients and plots data in dictio
        in 2 scatter plots, into savefile.png
    """
    LG_data = []
    dist_data = []
    no_dist_data = []
    for k, value in dictio.items():
        LG_data.append(value[0])
        dist_data.append(value[1])
        no_dist_data.append(value[2])

    # calculate Pearson's coefficient for each pair
    pearR_dist = np.corrcoef(LG_data, dist_data)[1,0]
    pearR_no_dist = np.corrcoef(LG_data, no_dist_data)[1,0]

    # scatter plots
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("FMI scatter-data")
    ax1.scatter(LG_data, dist_data, c = 'b', marker = '.', label = "R = %.4f"%(pearR_dist))
    ax1.set_title('LG vs Distance')
    ax1.set(xlabel = 'LG data', ylabel = 'window data')
    ax1.legend()
    ax1.axis('scaled')
    ax2.scatter(LG_data, no_dist_data, c = 'r', marker = '.', label = "R = %.4f"%(pearR_no_dist))
    ax2.set(xlabel = 'LG data')
    ax2.set_title('LG vs No-Distance')
    ax2.legend()
    ax2.axis('scaled')
    plt.savefig(savefile + ".png")

def main(argv):
    """
        Scatter-plots data in files and calculates Pearson's correlation
        coefficient between them.

        Usage: ./PearsonsCoeff.py -l <LG file> -d <distance file> 
               -n <no-distance file> -p <plotfile>

        LG file             file with LG any fmi
        distance file       file with window distance fmi
        no-distance file    file with window no-distance fmi
        plotfile            Name of ouputfile
    """

    version()

    LG_file = ''
    dist_file = ''
    no_dist_file = ''
    plot_file = ''

    try:
        opts, args = getopt.getopt(argv, "hl:d:n:p:", ["LGfile=", "distFile=",
         "noDistFile=", "plotfile="])
    except getopt.GetoptError:
        print("Usage: ./PearsonsCoeff.py -l <LG file> -d <distance file> -n <no-distance file> -p <plotfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: ./PearsonsCoeff.py -l <LG file> -d <distance file> -n <no-distance file> -p <plotfile>")
            sys.exit()
        elif opt in ("-l", "--LGfile"):
            LG_file = arg
        elif opt in ("-d", "--distFile"):
            dist_file = arg
        elif opt in ("-n", "--noDistFile"):
            no_dist_file = arg
        elif opt in ("-p", "--plotfile"):
            plot_file = arg

    LG_data = Load_File(LG_file)
    dist_data = Load_File(dist_file)
    no_dist_data = Load_File(no_dist_file)
    word_pair_dict = {}
    word_pair_dict = Increase_Dictionary(word_pair_dict, LG_data)
    word_pair_dict = Increase_Dictionary(word_pair_dict, dist_data)
    word_pair_dict = Increase_Dictionary(word_pair_dict, no_dist_data)
    Plot_Scatter(word_pair_dict, plot_file)

if __name__ == '__main__':
    main(sys.argv[1:])