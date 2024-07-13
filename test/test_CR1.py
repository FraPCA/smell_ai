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
    parser.add_argument("--compare",action="store_true", help="Enable comparison of different versions of a project")
    return parser

class TestCR1:
    def test_VR_1(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        assert args.compare is True

    def test_VE_1_1(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2
                
    def test_VE_1_2(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 3
        
    def test_VE_1_3(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2   
        
    def test_VE_1_4(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args)  
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert not (os.path.exists(str(fullpath) + "/1/to_save.csv")) #In tal caso, è avvenuto return per assenza di file.
        
    def test_VE_1_5(self, parse, tmp_path):    
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
        
        assert not os.path.exists(tempOutput / "project1" / "1") and not os.path.exists(tempOutput / "project2" / "1")
    
    def test_VE_1_6(self, parse, tmp_path):    
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
        if(os.path.exists(fullpath + "/1")):
            assert len(os.listdir(fullpath + "/1")) > 1
        else:
            assert False
            
    def test_VE_1_7(self, parse, tmp_path):    
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempFile = tempDir / "Non_Refactor_Smell_Examples.py"
        originalFile = '../input/projects/example/Non_Refactor_Smell_Examples.py'
        shutil.copyfile(originalFile, tempFile)       
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args) #Prima esecuzione
        analyzer.main(args) #Seconda esecuzione
        
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        if((os.path.exists(fullpath + "/1")) and (os.path.exists(fullpath + "/2"))):
            assert len(os.listdir(fullpath + "/2")) > 1
        else:
            assert False
        
    def test_VG_1_1(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2
                
    def test_VG_1_2(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 3
        
    def test_VG_1_3(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 2   
        
    def test_VG_1_4(self, parse, tmp_path):    
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
                
        args = parse.parse_args(["--input", str(tmp_path) + "/project", "--output", str(tempOutput), "--multiple", "True", "--compare"])
        
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 4
        
    def test_VG_1_5(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project"
        tempDir.mkdir()
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        with pytest.raises(SystemExit) as error:
            analyzer.main(args)
        assert error.value.code == 5   

    def test_VG_1_6(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempFile = tempDir / "Non_Refactor_Smell_Examples.py"
        originalFile = '../input/projects/example/Non_Refactor_Smell_Examples.py'
        shutil.copyfile(originalFile, tempFile)       
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args) #Prima esecuzione
        
        compareArgs = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        
        with pytest.raises(SystemExit) as error:
            analyzer.main(compareArgs)
        assert error.value.code == 6   
    
    def test_VG_1_7(self, parse, tmp_path):
        tempOutput = tmp_path / "output"
        tempOutput.mkdir()
        tempDir = tmp_path / "project/project1"
        tempDir.parent.mkdir()
        tempDir.mkdir()
        tempFile = tempDir / "Code_Smell_Examples.py"
        originalFile = '../input/projects/example/Code_Smell_Examples.py'
        shutil.copyfile(originalFile, tempFile)       
        args = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput)])
        analyzer.main(args) #Prima esecuzione
        refactorArgs = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--refactor"])
        analyzer.main(refactorArgs) #Seconda esecuzione
        analyzer.main(args) #Terza esecuzione
        
        compareArgs = parse.parse_args(["--input", str(tempDir), "--output", str(tempOutput), "--compare"])
        
        analyzer.main(compareArgs)
        fullpath = os.path.join(str(tempOutput), os.path.basename(os.path.normpath(args.input)))
        assert (os.path.exists(str(fullpath) + "/3/confronto_version.png")) and (os.path.exists(str(fullpath) + "/3/version.png"))