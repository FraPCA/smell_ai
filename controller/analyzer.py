import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor
from functools import reduce

import pandas as pd

from components import detector, graphic


def merge_results(input_dir="../output", output_dir="../general_output"):
    dataframes = []
    for subdir, dirs, files in os.walk(input_dir):
        if "to_save.csv" in files:
            df = pd.read_csv(os.path.join(subdir, "to_save.csv"))
            if len(df) > 0:
                dataframes.append(df)
                

    if dataframes:
        combined_df = pd.concat(dataframes)
        #rimuovi tutti le linee contenti filename,function_name,smell,name_smell,message tranne la prima
        combined_df = combined_df[combined_df["filename"] != "filename"]
        combined_df = combined_df.reset_index()


        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        combined_df.to_csv(os.path.join(output_dir, "overview_output.csv"), index=False)
    else:
        print("Error.")

def merge_refactor_results(input_dir="../output", output_dir="../general_output"):
    dataframes = []
    for subdir, dirs, files in os.walk(input_dir):
        if "R_to_save.csv" in files:
            df = pd.read_csv(os.path.join(subdir, "R_to_save.csv"))
            if len(df) > 0:
                dataframes.append(df)

    if dataframes:
        combined_df = pd.concat(dataframes)
        #rimuovi tutti le linee contenti filename,function_name,smell,name_smell,message tranne la prima
        combined_df = combined_df[combined_df["filename"] != "filename"]
        combined_df = combined_df.reset_index()


        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        combined_df.to_csv(os.path.join(output_dir, "overview_output.csv"), index=False)
    else:
        print("Error.")


def merge_times(input_dir="../output", output_dir="../general_output"):
    dataframes = []
    for subdir, dirs, files in os.walk(input_dir):
        if "analyzed_time.csv" in files:
            df = pd.read_csv(os.path.join(subdir, "analyzed_time.csv"))
            if len(df) > 0:
                dataframes.append(df)

    if dataframes:
        combined_df = pd.concat(dataframes)
        combined_df = combined_df[combined_df["filename"] != "filename"]
        combined_df = combined_df.reset_index()


        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        combined_df.to_csv(os.path.join(output_dir, "overview_times.csv"), index=False)
    else:
        print("Error.")
        
def find_python_files(url):
    try:
        # Estraiamo il path della directory radice del progetto e lo salaviamo in 'root'
        root = os.path.dirname(os.path.abspath(url))
        py_files = []
        # Attraversiamo ricorsivamente tutte le directory al di sotto della root
        for dirpath, _, filenames in os.walk(root):
            # Per ogni file all'interno della directory
            for f in filenames:
                # Se il file ha estensione .py, aggiungiamo il suo path assoluto alla lista 'py_files'
                if f.endswith('.py'):
                    py_files.append(os.path.join(dirpath, f))
        return py_files
    except Exception as e:
        print(f"Errore durante la ricerca dei file Python: {e}")


def get_python_files(path):
    result = []
    if os.path.isfile(path):
        if path.endswith(".py"):
            result.append(path)
            return result
    for root, dirs, files in os.walk(path):
        if "venv" in dirs:
            dirs.remove("venv")
        if "lib" in dirs:
            dirs.remove("lib")
        for file in files:
            if file.endswith(".py"):
                result.append(os.path.abspath(os.path.join(root, file)))
    return result


def analyze_project(project_path, output_path=".", refactor=False, Flag=True):
        
    col = ["filename", "function_name", "smell", "name_smell", "message"]
    r_col = ["filename", "function_name", "smell_name", "line"]
    to_save = pd.DataFrame(columns=col)
    empty_save = pd.DataFrame(columns=r_col)
    
    analysis_times = []
    
    #print("PATH OTTENUTO: " +project_path)
    
    filenames = get_python_files(project_path)
    
    if not any(File.endswith(".py") for File in filenames):
        print(f"La cartella {project_path} non contiene alcun file analizzabile al suo interno. Inserisci un altro path in input.")
        return
    
    if refactor:
        if not os.path.exists(output_path + "\Ref"):
            os.makedirs(output_path + "\Ref")
    
    #print("Ottenuti filename")
    
    #print(filenames)
    
    for filename in filenames:
        if "tests/" not in filename:  # ignore test files
            try:
                #print("Prima di detector inspect")
                singleTimer = time.time()
                print("Analizzo " + filename)
                result = detector.inspect(filename, output_path, refactor)
                to_save = to_save.merge(result, how='outer')
                totalTime = time.time() - singleTimer
                print("Tempo di esecuzione: " + str(totalTime))
                analysis_times.append({"filename": filename, "time": totalTime})
                
            except SyntaxError as e:
                message = e.msg
                error_path = output_path
                if not os.path.exists(error_path):
                    os.makedirs(error_path)
                with open(f"{error_path}/error.txt", "a") as error_file:
                    error_file.write(message)
                continue
            except FileNotFoundError as e:
                message = e
                error_path = output_path
                if not os.path.exists(error_path):
                    os.makedirs(error_path)
                with open(f"{error_path}/error.txt", "a") as error_file:
                    error_file.write(str(message))
                continue

    to_save.to_csv(output_path + "/to_save.csv", index=False, mode='a')
    if refactor:
        if len(os.listdir(output_path + "\Ref")) != 0:
            all_csvs = [pd.read_csv(output_path + "\Ref\\" + file) for file in os.listdir(output_path + "\Ref") if file.endswith(".csv")]
            rdf = pd.concat(all_csvs, ignore_index=True)
            rdf.to_csv(output_path + "\Ref" + "/R_to_save.csv", index=False, mode='a')
        else:
            empty_save.to_csv(output_path + "\Ref" + "/R_to_save.csv", index=False, mode='a')

    analyzed_time = pd.DataFrame(analysis_times, columns=["filename", "time"])
    analyzed_time.to_csv(output_path + "/analyzed_time.csv", index=False, mode='a')
    graphic.graph(output_path, Flag)
    graphic.grafico_barre(output_path, Flag)
    graphic.grafico_dispersione(output_path, Flag)

def projects_analysis(base_path='../input/projects', output_path='../output/projects_analysis',resume=False,refactor=False):
    start = time.time()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    dirpath = os.listdir(base_path)
    if not os.path.exists("../config/execution_log.txt"):
        #get abs path of execution_log.txt
        execution_log_path = os.path.abspath("../config/execution_log.txt")
        #print("Path:"+execution_log_path)
        open("../config/execution_log.txt", "w").close()
        resume = False
    execution_log = open("../config/execution_log.txt", "a")
    #get last project analyzed in execution_log.txt
    if resume:
        with open("../config/execution_log.txt", "r") as f:
            last_project = f.readlines()[-1]
    for dirname in dirpath:
        if resume:
            if dirname <= last_project:
                continue
        new_path = os.path.join(base_path, dirname)
        if not os.path.exists(f"{output_path}/{dirname}"):
            os.makedirs(f"{output_path}/{dirname}")
        print(f"Analyzing {dirname}...")
        singleTimer = time.time()
        analyze_project(new_path, f"{output_path}/{dirname}", refactor, False)
        print(f"{dirname} analyzed successfully.")
        print(f"Exec Time completed in: {time.time() - singleTimer}")
        execution_log.write(dirname + "\n")
    end = time.time()
    print(f"Sequential Exec Time completed in: {end - start}")


def parallel_projects_analysis(base_path='../input/projects', output_path='../output/projects_analysis', max_workers=5,resume=False,refactor=False):
    start = time.time()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        dirpath = os.listdir(base_path)
        for dirname in dirpath:
            new_path = os.path.join(base_path, dirname)
            if not os.path.exists(f"{output_path}/{dirname}"):
                os.makedirs(f"{output_path}/{dirname}")
            executor.submit(analyze_project, new_path, f"{output_path}/{dirname}")
    end = time.time()
    print(f"Parallel Exec Time completed in: {end - start}")


def clean(output_path="../output/projects_analysis"):
    # check os windows or linux

    if os.name == "nt":
        clean_win_path = output_path.replace("/", "\\")
        if os.path.exists(clean_win_path):
            os.system(f"rmdir /s /q {clean_win_path}")

    else:
        if os.path.exists(output_path):
            os.system(f"rm -r {output_path}")



def main(args):
    print(args.input)
    print(args.output)

    if args.input is None or args.output is None:
        print("Please specify input and output folders")
        exit(1)
        
    if not os.path.isdir(args.input):
        print(f"La cartella {args.input} non esiste. Inserisci un altro path in input.")
        exit(2)

    if not os.path.isdir(args.output):
        print(f"La cartella {args.output} non esiste. Inserisci un altro path di output.")
        exit(3)
        
    resume = True

    multiple = args.multiple
    refactor = args.refactor
    compare = args.compare

    if compare:
        if multiple:
            print("Si possono comparare più versioni solo di un singolo progetto")
            return
        fullpath = os.path.join(args.output, os.path.basename(os.path.normpath(args.input)))
        if not os.path.exists(fullpath):
            print("Non è stata trovata alcuna versione del progetto da confrontare")
            return
        if len(os.listdir(fullpath)) > 1:
            graphic.grafico_curva(fullpath)
            graphic.grafico_orizzontale(fullpath)
            return
        else:
            print("Non è possibile effettuare la comparazione")
            return
    if multiple:
        if not args.resume:
            resume = False
            clean(args.output)
        if args.parallel:
            parallel_projects_analysis(args.input, args.output, args.max_workers,resume, refactor)
        else:
            if not os.path.exists(f"{args.output}"):
                os.makedirs(f"{args.output}")
            projects_analysis(args.input, args.output,resume, refactor)
    else:

        fullpath = os.path.join(args.output, os.path.basename(os.path.normpath(args.input)))
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
            version = os.path.join(fullpath , "1")
            os.makedirs(version)
        else:
            dirpath = os.listdir(fullpath)
            lastversion = 0
            for dirname in dirpath:
                vernumber = int(dirname)
                if vernumber > lastversion:
                    lastversion = vernumber
            version = os.path.join(fullpath,str(lastversion + 1))
            os.makedirs(version)
        analyze_project(args.input, version, refactor)
    merge_results(args.output, args.output+"/overview")
    merge_times(args.output, args.output+"/time")
    if refactor:
        merge_refactor_results(args.output, args.output + "/R_overview")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Smile is a tool for detecting AI-specific code smells "
                                                 "for Python projects")
    parser.add_argument("--input", type=str, help="Path to the input folder")
    parser.add_argument("--output", type=str, help="Path to the output folder")
    parser.add_argument("--max_workers", type=int, default=5,help="Number of workers for parallel execution")
    parser.add_argument("--parallel",default=False, type=bool, help="Enable parallel execution")
    parser.add_argument("--resume", default=False, type=bool, help="Continue previous execution")
    parser.add_argument("--multiple", default=False, type=bool, help="Enable multiple projects analysis")
    parser.add_argument("--refactor", action = "store_true", help="Enable refactoring of found smells")
    parser.add_argument("--compare",action="store_true", help="Enable comparison of different versions of a project")
    args = parser.parse_args()
    main(args)



