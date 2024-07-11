import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm


def graph(out_path, Flag):

    path = out_path + "/to_save.csv"
    # Leggere i dati dal file CSV
    df = pd.read_csv(path)

    # Contare il numero di occorrenze di ciascun tipo di "smell"
    smell_counts = df['name_smell'].value_counts()

    # Preparare le etichette senza underscore e spazi
    labels = [label.replace('_', ' ') for label in smell_counts.index]

    # Creare il grafico a torta e ottenere i colori degli spicchi
    plt.figure(figsize=(10, 7))
    patches, texts, autotexts = plt.pie(smell_counts, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 7})

    # Ottenere i colori degli spicchi
    colors = [patch.get_facecolor() for patch in patches]

    # Applicare i colori alle etichette
    for text, color in zip(texts, colors):
        text.set_color(color)

    # Aggiungere un titolo
    plt.suptitle('Distribuzione dei Code Smells nel Progetto', y=0.95, fontsize=14)

    # Assicurarsi che il grafico sia un cerchio
    plt.axis('equal')

    # Salvare il grafico come file immagine con bordi stretti per evitare tagli
    output_image_path = 'smell_distribution_pie_chart.png'
    plt.savefig(str(os.path.join(out_path, output_image_path)), bbox_inches='tight')

    # Visualizzare il grafico
    if(Flag):
        plt.show()

def grafico_barre(out_path, Flag):

    path = out_path + "/to_save.csv"
    #print("PATH GRAFICO A BARRE" + path)

    # Leggere i dati dal file CSV
    df = pd.read_csv(path)

    # Estrarre solo la parte desiderata del percorso del file
    df['short_filename'] = df['filename'].apply(lambda x: os.path.join(*x.split(os.sep)[-2:]))

    # Contare il numero di smell per ciascun file
    smell_counts = df['short_filename'].value_counts()

    # Generare una lista di colori usando una mappa di colori
    colormap = cm.get_cmap('Pastel2', len(smell_counts))  # Scegliere una mappa di colori
    colors = [colormap(i) for i in range(len(smell_counts))]

    # Creare il grafico a barre
    plt.figure(figsize=(12, 6))
    bar_plot = smell_counts.plot(kind='bar', color= colors)
    bar_plot.margins(0,2)

    # Aggiungere etichette e titolo
    plt.xlabel('File')
    plt.ylabel('Numero di Smell')
    plt.title('Numero di Smell Rilevati per File', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Annotare le barre con il numero di smell
    for index, value in enumerate(smell_counts):
        bar_plot.text(index, value / 2 , str(value), ha='center', va='center', fontsize=10, color= 'black')
    plt.tight_layout()

    # Salvare il grafico come file immagine
    output_image_path = 'smell_counts_bar_chart.png'
    plt.savefig(str(os.path.join(out_path, output_image_path)), bbox_inches='tight')

    # Visualizzare il grafico
    if(Flag):
        plt.show()



def grafico_dispersione(out_path, Flag):
    
    path = out_path + "/to_save.csv"
    path1 = out_path + "/analyzed_time.csv"

        
    df = pd.read_csv(path)
    df2 = pd.read_csv(path1)

    # Estrarre solo la parte desiderata del percorso del file
    df['short_filename'] = df['filename'].apply(lambda x: os.path.join(*x.split(os.sep)[-2:]))

    smell_counts = df['short_filename'].value_counts().reset_index()
    smell_counts.columns = ['short_filename', 'smell_count']

    df2['short_filename'] = df2['filename'].apply(lambda x: os.path.join(*x.split(os.sep)[-2:]))

    # Unire i due dataframe basati sul nome del file
    merged_df = pd.merge(smell_counts, df2, on='short_filename')

    # Creare il grafico a dispersione
    plt.figure(figsize=(12, 6))
    
    # Utilizzare la palette di colori Pastel2
    colormap = cm.get_cmap('tab20', len(merged_df))
    colors = [colormap(i) for i in range(len(merged_df))]
    
    # Creare il grafico a dispersione con colori diversi per ciascun punto
    scatter = plt.scatter(merged_df['smell_count'], merged_df['time'], color=colors)

    # Aggiungere etichette e titolo
    plt.xlabel('Numero di Smell Individuati')
    plt.ylabel('Tempo di Analisi (s)')
    plt.title('Tempo di Analisi vs Numero di Smell Individuati per File', pad = 20)


    # Creare la legenda con i nomi dei file e i colori corrispondenti
    for i, txt in enumerate(merged_df['short_filename']):
        plt.plot([], [], color=colors[i], label=txt)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)

    plt.tight_layout()

    # Salvare il grafico come file immagine
    output_image_path = 'smell_time_scatter_plot.png'
    plt.savefig(str(os.path.join(out_path, output_image_path)), bbox_inches='tight')

    # Visualizzare il grafico
    if(Flag):
        plt.show()


def grafico_curva(path):

    dirpath = os.listdir(path)
    smell_counts = {}

    for dirname in dirpath:
        nuovo_path = os.path.join(path, dirname)
        file_path = os.path.join(nuovo_path, "to_save.csv")
        df = pd.read_csv(file_path,header = None)
        total_smell = len(df.axes[0]) - 1
        smell_counts[dirname] = total_smell

    sorted_smell_counts = dict(sorted(smell_counts.items()))

    # Crea il grafico a curva
    plt.figure(figsize=(10, 6))
    plt.plot(list(sorted_smell_counts.keys()), list(sorted_smell_counts.values()), marker='o')
    plt.xlabel('Sottocartelle')
    plt.ylabel('Numero Totale di Smell')
    plt.title('Numero Totale di Smell per Sottocartella')
    plt.xticks(rotation=45)
    plt.grid(True)
    # Salvare il grafico come file immagine
    output_image_path = 'version.png'
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.show()

def grafico_orizzontale(path):
    
    
    dirpath = os.listdir(path)
    lastversion = 0
    for dirname in dirpath:
        vernumber = int(dirname)
        if vernumber > lastversion:
            lastversion = vernumber
    
    version = os.path.join(path,str(lastversion))
    pen_version = os.path.join(path,str(lastversion - 1))

    file_version = os.path.join(version, "to_save.csv")
    filepen_version = os.path.join(pen_version, "to_save.csv")

    df = pd.read_csv(filepen_version, header=None, names=["filename", "function_name", "smell", "name_smell", "message"])
    df2 = pd.read_csv(file_version, header=None, names=["filename", "function_name", "smell", "name_smell", "message"])
    smell_count = df['name_smell'].value_counts().to_dict()
    smell_count2 = df2['name_smell'].value_counts().to_dict()

    all_smells = set(smell_count.keys()).union(set(smell_count2.keys()))

    smells = sorted(all_smells)
    counts1 = [smell_count.get(smell, 0) for smell in smells]
    counts2 = [smell_count2.get(smell, 0) for smell in smells]

    

    # Crea il grafico a barre orizzontali
    fig, ax = plt.subplots(figsize=(10, 8))
    bar_width = 0.4
    y_pos = range(len(smells))

    colors = cm.get_cmap('Pastel2')(range(len(smells)))

    ax.barh(y_pos, counts1, bar_width, label="Penultima Versione", color=colors[0])
    ax.barh([p + bar_width for p in y_pos], counts2, bar_width, label="Ultima versione", color=colors[1])
    
    ax.bar_label(ax.containers[0], label_type='edge', padding = 5)
    ax.bar_label(ax.containers[1], label_type='edge', padding = 5)
    
    ax.set_yticks([p + bar_width / 2 for p in y_pos])
    ax.set_yticklabels(smells, fontsize = 7)
    ax.set_xlabel('Numero di occorrenze')
    ax.set_title('Confronto dei Code Smells tra due cartelle')
    ax.legend()
    

    # Aggiunge margini per assicurarsi che le etichette non vengano tagliate
    plt.tight_layout()
    # Salvare il grafico come file immagine
    output_image_path = 'confronto_version.png'
    plt.savefig(output_image_path, bbox_inches='tight')

    plt.show()









