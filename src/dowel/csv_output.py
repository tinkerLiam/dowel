"""A `dowel.logger.LogOutput` for CSV files."""
import csv
import warnings
import time
import shutil
import os

from dowel import TabularInput

from dowel.simple_outputs import FileOutput
from dowel.utils import colorize



class CsvOutput(FileOutput):
    """CSV file output for logger.

    :param file_name: The file this output should log to.
    """

    def __init__(self, file_name):
        super().__init__(file_name)
        self._writer = None
        self._fieldnames = None
        self._warned_once = set()
        self._disable_warnings = False
        self._file_name=file_name
        
    @property
    def types_accepted(self):
        """Accept TabularInput objects only."""
        return (TabularInput, )


    def record(self, data, prefix=''):
        """Log tabular data to CSV."""
        if isinstance(data, TabularInput):
            to_csv = data.as_primitive_dict

            if not to_csv.keys() and not self._writer:
                return
            
            if to_csv.keys() != self._fieldnames:
                self._fieldnames=to_csv.keys()
                self.reorganize_file(data)        

            self._writer = csv.DictWriter(
                self._log_file,
                fieldnames=self._fieldnames,
                extrasaction='ignore')
            self._writer.writerow(to_csv)

            for k in to_csv.keys():
                data.mark(k)

        else:
            raise ValueError('Unacceptable type.')


    def reorganize_file(self,data):
        """After some adjustments for TabularInput,
        we can leave the cell blank, if the value of the key is missing
        
        Thus, next goal is to expand header
        ,and expand old rows with empty cells for the new key

        """
        temp_file=str(int(time.time()*1000))
        with open(temp_file,'w+') as ft:
            ft_writer=csv.DictWriter(ft, fieldnames=self._fieldnames)
            ft_writer.writeheader()

            with open(self._file_name, 'r') as f:
                f_csv=csv.DictReader(f)
                for row in f_csv:
                    ft_writer.writerow(row)
                        
        shutil.copyfile(temp_file,self._file_name)
        self._log_file = open(self._file_name, 'a')
        os.remove(temp_file)

    def _warn(self, msg):
        """Warns the user using warnings.warn.

        The stacklevel parameter needs to be 3 to ensure the call to logger.log
        is the one printed.
        """
        if not self._disable_warnings and msg not in self._warned_once:
            warnings.warn(
                colorize(msg, 'yellow'), CsvOutputWarning, stacklevel=3)
        self._warned_once.add(msg)
        return msg

    def disable_warnings(self):
        """Disable logger warnings for testing."""
        self._disable_warnings = True


class CsvOutputWarning(UserWarning):
    """Warning class for CsvOutput."""

    pass
