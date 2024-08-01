# Script by Youssef El Gharably, written to create publishable figures based on CLASS 
# text files. 
# You can launch this from the terminal without having to worry about anything :D
# Written on July 30th

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
import os
from tkinter import filedialog

# This function takes in the CLASS text files and returns a data frame of it
def df_builder(file):
    df = pd.read_csv(file, delim_whitespace=True, header=None)
    df.columns = ['Velocity','Intensity']
    df['Intensity'] = df['Intensity']*1000 # Convert to millikelvins
    return df

# This script will be entering a directory the user specifies and should essentially do all the work by itself
# Assuming the text files are named as follow: SOURCENAME_MOLECULE_TRANSITION.txt
# ex: "IRAS05113+1347_HCN_32" for source IRAS05113+1347 with an observation of J=3-2 (IN THAT ORDER) of HCN.
# By making a list of data frames for each source, this will make the plotting process significantly easier

# The following three functions are ones I wrote previously for AGN research to navigate 
# files in a directory properly on a Windows OR Mac Machine.
def get_directory_path():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Directory Containing CLASS text files:")
    return directory.replace("\\", "/")

def get_root_from_directory(directory):
    unprocessed_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            unprocessed_files.append(os.path.join(root, file).replace("\\", "/"))
    return np.sort(unprocessed_files)

def get_unique_file_names(file_paths):
    file_names = set()  # avoiding repeats
    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_names.add(file_name)
    return np.sort(list(file_names))

# Please keep in mind that the list is sorted, and the program relies on the initial placement and order
# of all the list elements. So for index 1 in source, the program expects index 1 in molecule to correspond 
# to it.
def name_splitter(names):
    source = []
    molecule = []
    transition = []
    for name in names:
        parts = name.split('_')
        source.append(parts[0])
        molecule.append(parts[1])
        transition.append(parts[2])
    return source,molecule,transition

def vlsr(file):
    df = pd.read_csv(file, delim_whitespace=False, header=None, delimiter=',')
    df.columns = ['Source','vlsr']
    return df

# This function takes in a data frame with its corresponding source name, molecule, and transition then
# plots them together for each single source
def plot_source(df_list,source,molecule,transition,vlsr):
    arrow = r'$\rightarrow$'
    fig, axs = plt.subplots(len(molecule), 1, figsize=(6,len(molecule)*3), sharex=True)
    fig.suptitle(f"{source[0]}", fontsize=24, fontname='Arial', fontweight='bold')
    for i in range(len(molecule)):
        axs[i].step(df_list[i]['Velocity'], df_list[i]['Intensity'], color='black',linewidth=0.7)
        axs[i].text(0.80, 0.95, f"{molecule[i]}", 
                    transform=axs[i].transAxes, verticalalignment='top', horizontalalignment='left',fontweight='bold',fontsize=16)
        axs[i].text(0.80, 0.85, f"J={transition[i][0]}{arrow}{transition[i][1]}", 
                    transform=axs[i].transAxes, verticalalignment='top', horizontalalignment='left',fontsize=14)
        axs[i].set_xlim(vlsr-150,vlsr+150)
        central_tick = vlsr
        ticks = [vlsr - 150, vlsr - 100, vlsr - 50, central_tick, vlsr + 50, vlsr + 100, vlsr + 150]
        axs[i].set_xticks(ticks)
        axs[i].tick_params(right=True, left=True,axis='y',color='k',length=6,direction='in')
        axs[i].tick_params(axis='x',which='both', direction='in', color='k', length=6, width=1)
        axs[i].tick_params(axis='x', labelsize=14)
        axs[i].tick_params(axis='y', labelsize=14)
    plt.xlabel(r'V$_{LSR}$ (km s$^{-1}$)',fontsize=16,fontweight='bold')
    fig.text(0.035, 0.5, r"$T_A^*$ (mk)", va='center', ha='center', rotation='vertical', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.subplots_adjust(left=0.12)
    plt.show()

def main():
    directory = get_directory_path()
    files_path = get_root_from_directory(directory)
    file_names = get_unique_file_names(files_path)
    sources, molecule, transition = name_splitter(file_names)
    #print(f"sources = {sources}\nmolecule = {molecule}\ntransition = {transition}")
    unique_sources = list(set(sources))
    #print(f"unique_sources = {unique_sources}")

    vlsr_path = r"D:\Undergraduate Life\Summer 2024\HCN_HCO\Text Files\vlsr_list.txt"
    vlsr_df = vlsr(vlsr_path)

    for source in unique_sources:
        df_list = []
        source_list = []
        molecule_list = []
        transition_list = []
        for i in range(len(files_path)):
            if source in files_path[i]:
                source_list.append(sources[i])
                molecule_list.append(molecule[i])
                transition_list.append(transition[i])
                df_list.append(df_builder(files_path[i]))
        #print(f"df_list = {df_list}\nsource_list = {source_list}\n molecule_list = {molecule_list}\n transition_list = {transition_list}")
        plot_source(df_list,source_list,molecule_list,transition_list,float(vlsr_df.loc[vlsr_df['Source'] == source, 'vlsr'].values[0]))

if __name__ == "__main__":
    main()

            


        

