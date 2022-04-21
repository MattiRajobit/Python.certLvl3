
from robot.libraries.BuiltIn import BuiltIn
from RPA.Robocorp.WorkItems import WorkItems 
localOut=r"C:\Users\matti\Documents\RBCORP\Etuovi\output\results"
service_account = r"C:\Users\matti\Downloads\service_account.json"
try:
    outDir=BuiltIn().get_variable_value("${OUTPUT_DIR}")
    if(outDir):
        OUTPUT_PATH=outDir
    else:
        OUTPUT_PATH=localOut
except Exception as e:
    print(e)
    OUTPUT_PATH=localOut
try:
    WORKITEMS=BuiltIn().get_library_instance("RPA.Robocorp.WorkItems")
except Exception as e:
    WORKITEMS=WorkItems()

class Configs():
    def SetOUTPUT(self,output):
        global OUTPUT_PATH
        OUTPUT_PATH=output
