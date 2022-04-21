from robot.api import logger
import robot
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import robot.libraries.Screenshot as sc
def example3(expected_data):
    logger.info("example3!")


class MyLibrary:
    """Give this library a proper name and document it."""

    def example2_python_keyword(self,expected_data=""):
        logger.info("example2!")
    def example_python_keyword(self):
        path=sc.Screenshot().take_screenshot()
        logger.info(path)
        logger.info("This is Python!")
        logger.info("Lisää äöäöäöä!")
        self.example2_python_keyword("hahaa")
        example3("sada")
        BuiltIn().run_keyword(name="Example keyword3")
        #TÄmä tekee logi merkinnän
        BuiltIn().run_keyword(name="MyLibrary.Example2 Python Keyword")
        #Tämä ei tee logi merkintää
        BuiltIn().call_method(object=self,method_name="example2_python_keyword")
    def keyword(self,log_level="INFO"):
        """Does something and logs the output using the given level.


        Valid values for log level` are "INFO" (default) "DEBUG" and "TRACE".

        See also `Another Keyword`.
        """
        # ...
        logger.info("keywordiiiii")

    def another_keyword(self,argument, log_level="INFO"):
        """Does something with the given argument else and logs the output.

        See `Keyword` for information about valid log levels.
        """
        logger.info("another_keyword")

if __name__ == "__main__":
    print("")
    screen=sc.Screenshot()
    path=sc.Screenshot().take_screenshot()