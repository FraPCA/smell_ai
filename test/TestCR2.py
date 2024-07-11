import shutil
from controller import analyzer
from components import detector
from cs_detector.detection_rules import Generic, APISpecific
from cs_detector.refactor_rules import Generic, APISpecific

import os, pytest, argparse, pandas

@pytest.fixture 
def parse():
    parser = argparse.ArgumentParser(description="Code Smile is a tool for detecting AI-specific code smells for Python projects")
    parser.add_argument("--input", type=str, help="Path to the input folder")
    parser.add_argument("--output", type=str, help="Path to the output folder")
    parser.add_argument("--max_workers", type=int, default=5,help="Number of workers for parallel execution")
    parser.add_argument("--parallel",default=False, type=bool, help="Enable parallel execution")
    parser.add_argument("--resume", default=False, type=bool, help="Continue previous execution")
    parser.add_argument("--multiple", default=False, type=bool, help="Enable multiple projects analysis")
    parser.add_argument("--refactor", action = "store_true", help="Enable refactoring of found smells")
    return parser

class TestCR2:
        
    def test_PT_1_1(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2
                
    def test_PT_1_2(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 3
        
    def test_PT_1_3(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2   
        
    def test_PT_1_4(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args)  
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert not (os.path.exists(str(fullpath) + "/1/to_save.csv")) #In tal caso, è avvenuto return per assenza di file.
        
    def test_PT_1_5(self, parse, tmp_path):    
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempFile = tempDir / "Non_Refactor_Smell_Examples.py"
        originalFile = '../input/projects/example/Non_Refactor_Smell_Examples.py'
        shutil.copyfile(originalFile, tempFile)       
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args)
        
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert ((os.path.exists(str(fullpath) + "/1/analyzed_time.csv")) and (os.path.exists(tempOutput / "time"/ "overview_times.csv")))


        
    def test_PT_1_6(self, parse, tmp_path):    
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempDir2 = tmp_path / "project/project2"
        tempDir2.mkdir()
        
        tempFile1 = tempDir / "Non_Refactor_Smell_Examples.py"
        tempFile2 = tempDir2 / "Code_Smell_Examples.py"
        
        originalFile1 = '../input/projects/example/Non_Refactor_Smell_Examples.py'
        originalFile2 = '../input/projects/example/Code_Smell_Examples.py'
        shutil.copyfile(originalFile1, tempFile1)
        shutil.copyfile(originalFile2, tempFile2)        
                
        args = parse.parse_args(["--input", str(tmp_path) + "/project", "--output", str(tempOutput), "--multiple", "True"])
        analyzer.main(args)
        
        if(os.path.exists(tempOutput / "project1" / "analyzed_time.csv") and os.path.exists(tempOutput / "project2" / "analyzed_time.csv")):
            assert (os.path.exists(tempOutput / "time/overview_times.csv"))
        else:
            assert False
                
    def test_PG_1_1(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2
                
    def test_PG_1_2(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 3
        
    def test_PG_1_3(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2   
        
    def test_PG_1_4(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args)  
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert not (os.path.exists(str(fullpath) + "/1/to_save.csv")) #In tal caso, è avvenuto return per assenza di file.
        
    def test_PG_1_5(self, parse, tmp_path):    
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempFile = tempDir / "Non_Refactor_Smell_Examples.py"
        originalFile = '../input/projects/example/Non_Refactor_Smell_Examples.py'
        shutil.copyfile(originalFile, tempFile)       
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args)
        
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert ((os.path.exists(str(fullpath) + "/1/smell_counts_bar_chart.png")) and (os.path.exists(str(fullpath) + "/1/smell_distribution_pie_chart.png")) and (os.path.exists(str(fullpath) + "/1/smell_time_scatter_plot.png"))) 


        
    def test_PG_1_6(self, parse, tmp_path):    
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempFile1 = tempDir / "Non_Refactor_Smell_Examples.py"
        tempFile2 = tempDir / "Single_Smell_Non_Refactor_Example.py"
        tempFile3 = tempDir / "Code_Smell_Examples.py"
        originalFile1 = '../input/projects/example/Non_Refactor_Smell_Examples.py'
        originalFile2 = '../input/projects/example/Single_Smell_Non_Refactor_Example.py'
        originalFile3 = '../input/projects/example/Code_Smell_Examples.py'
        shutil.copyfile(originalFile1, tempFile1)
        shutil.copyfile(originalFile2, tempFile2)        
        shutil.copyfile(originalFile3, tempFile3)                
        args = parse.parse_args(["--input", str(tmp_path), "--output", str(tempOutput)])
        analyzer.main(args)
        
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert ((os.path.exists(str(fullpath) + "/1/smell_counts_bar_chart.png")) and (os.path.exists(str(fullpath) + "/1/smell_distribution_pie_chart.png")) and (os.path.exists(str(fullpath) + "/1/smell_time_scatter_plot.png"))) 