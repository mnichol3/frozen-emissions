"""
Tests that insure only combustion-related sectors have been "frozen" (read: modified)

Matt Nicholson
13 Feb  2020
"""
import unittest
import sys
import os
import pandas as pd

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import emission_factor_file
import test_utils
import driver

class TestInit(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = 'input/config-test_frozen_sectors.yml'
        self.species = 'BC'
        # Initialize global CONFIG object
        config.CONFIG = config.ConfigObj(self.f_init)
        # Use an un-edited CMIP6 EF file as a control
        self.f_control = r"C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output"
        # Freeze and calculate emissions
        driver.freeze_emissions()
        driver.calc_emissions()
        # Read the frozen emissions in to a dataframe
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.f_frozen = os.path.join(config.CONFIG.dirs['inter_out'], self.f_ef)
        self.frozen_df = pd.read_csv(self.f_frozen, sep=',', header=0)
        
    def test_frozen_sectors(self):
        """Check that only combustion-related sectors were modified
        """
        # Read the un-edited control CMIP6 EF file
        control_path = os.path.join(self.f_control, self.f_frozen)
        control_df = pd.read_csv(control_path, sep=',', header=0)
        # Get a subset of the control & frozen DF containing only non-combustion sectors
        control_non_combust = control_df.loc[control_df['sector'].isin(test_utils.non_combustion_sectors)].copy()
        frozen_non_combust = self.frozen_df.loc[self.frozen_df['sector'].isin(test_utils.non_combustion_sectors)].copy()
        self.assertTrue(control_non_combust.equals(frozen_non_combust))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()