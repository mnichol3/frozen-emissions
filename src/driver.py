"""
Main script that produces the frozen emissions

Matt Nicholson
7 Feb 2020
"""
# import logging
import argparse
import logging
import os
import pandas as pd

import log_config
import ceds_io
import config
import z_stats
import emission_factor_file

def init_parser():
    """
    Initialize a new argparse parser
    
    Parameters
    -----------
    None
    
    Return
    -------
    argparse.ArgumentParser object
    
    Args
    -----
    input_file; str
        Path of the input YAML file. This argument is required.
    -f, --function; str, optional
        Function (out of "freeze_emissions" & "calc_emissions") to execute.
        Default is to execute both functions. 
        Example: Recalculate final emissions only
            > python main.py path/to/yaml -f "calc_emissions"
    """
    parse_desc = """Freeze CEDS CMIP6 emissions factors and calculate frozen total emissions"""
    
    parser = argparse.ArgumentParser(description=parse_desc)
    
    parser.add_argument(metavar='input_file', dest='input_file',
                        action='store', type=str,
                        help='Path of the input YAML file')
                        
    parser.add_argument('-f', '--function', metavar='function', required=False,
                        dest='function', action='store', type=str, default='all',
                        help=('Optional; Function(s) to execute ("freeze_emissions" or "calc_emissions").'
                              'Default value is "both", which executes both functions'))
    return parser


def freeze_emissions():
    """
    Freeze emissions factors for years >= 'year'
    
    'Freezing' the emissions factors means setting the values for years > a given
    year equal to their value for that year. For example, freezing emissions factors
    at 1970 means the emissions factors for years 1971-present are set to their
    1970 value
    
    Parameters
    -----------
    None, uses global CONFIG object
    
    Return
    -------
    None
    """
    failed_species = [''] * len(config.CONFIG.freeze_species)
    fail_idx = 0
    
    # Unpack config directory paths for better readability
    dir_cmip6 = config.CONFIG.dirs['cmip6']
    dir_output = config.CONFIG.dirs['output']
    
    logger = logging.getLogger("main")
    logger.info("In main::freeze_emissions()")
    logger.info("dir_cmip6 = {}".format(dir_cmip6))
    logger.info("freeze year = {}\n".format(config.CONFIG.freeze_year))
        
    # Construct the column header strings for years >= 'year' param
    year_strs = ['X{}'.format(yr) for yr in range(config.CONFIG.freeze_year,
                                                  config.CONFIG.ceds_meta['year_last'] + 1)]
    
    # Begin for-loop over each species we want to freeze
    for species in config.CONFIG.freeze_species:
        logger.info("Processing species: {}".format(species))
        
        # Get the species' EF file
        try:
            f_path = ceds_io.get_file_for_species(dir_cmip6, species, "ef")
        except FileNotFoundError as err:
            # If a FileNotFoundError is returned, log it and move on to the next species
            err_str = "Error encountered while fetching EF file: {}".format(err)
            logger.error(err_str)
            failed_species[fail_idx] = species
            fail_idx += 1
            continue

        logger.info("Loading EF DataFrame from {}".format(f_path))
        # ef_df = ceds_io.read_ef_file(f_path)
        ef_obj = emission_factor_file.EmissionFactorFile(species, f_path)
        
        # Get combustion sectors
        sectors = ef_obj.get_sectors()
        fuels = ef_obj.get_fuels()
        
        for sector in sectors:
            for fuel in fuels:
                info_str = "Processing {}...{}...{}".format(species, sector, fuel)
                logger.info("--- {} ---".format(info_str))
                print("{}...".format(info_str))
                
                if (ef_obj.get_comb_shape()[0] != 0):
                    # Calculate the median of the EF values
                    ef_median = z_stats.get_ef_median(ef_obj)
                    logger.debug("EF data array median: {}".format(ef_median))
                    logger.debug("Identifying outliers")
                    
                    outliers = z_stats.get_outliers_zscore(ef_obj, sector, fuel)
                    if (len(outliers) != 0):
                        logger.debug("Setting outlier values to median EF value")
                        # Set the EF value of each idenfitied outlier to the median of the EF values
                        for olr in outliers:
                            # Set outlier values to the calculated median val
                            ef_obj.combustion_factors.loc[
                                    (ef_obj.combustion_factors['iso'] == olr[0]) &
                                    (ef_obj.combustion_factors['sector'] == sector) &
                                    (ef_obj.combustion_factors['fuel'] == fuel) &
                                    (ef_obj.combustion_factors[ef_obj.freeze_year] == olr[1])
                                    ] = ef_median
                    else:
                        logger.debug("No outliers were identified")
                    # Overwrite the current EFs for years >= 1970
                    logger.debug("Overwriting original EF DataFrame with new EF values")
                else:
                    logger.warning("Subsetted EF dataframe is empty")
            # --- End fuel loop ---
        # --- End sector loop ---
        # Freeze the combustion emissions
        logger.debug("Freezing emissions...")
        ef_obj.freeze_emissions(year_strs)
        
        # Overwrite the corresponding values from the original EF DataFrame
        logger.debug("Reconstructing total emissions factors DataFrame...")
        ef_obj.reconstruct_emissions()
        
        f_name = os.path.basename(f_path)
        f_out = os.path.join(dir_output, f_name)
        
        info_str = "Writing frozen emissions factors DataFrame to {}".format(f_out)
        logger.debug(info_str)
        print(info_str + '\n')
        
        ef_obj.all_factors.to_csv(f_out, sep=',', header=True, index=False)
        logger.info("--- Finished processing {} ---\n".format(species))
        
    # --- End EF file for-loop ---
    [logger.warning('Emissions calculation failed for {}'.format(failure))
            for failure in failed_species if failure != '']
    logger.info("Finished processing all species\nLeaving main::freeze_emissions()\n")
    
    
def calc_emissions():
    """
    Calculate the hypothetical emissions from the frozen emissions and the CMIP6
    activity files
    
    Emissions = EF x Activity
    
    Parameters
    -----------
    None, uses global CONFIG object
        
    Return
    -------
    None, writes to file
    """
    failed_species = [''] * len(config.CONFIG.freeze_species)
    fail_idx = 0
    
    logger = logging.getLogger("main")
    logger.info('In main::calc_emissions()')
    
    # Unpack for better readability
    dir_output = config.CONFIG.dirs['output']
    dir_cmip6 = config.CONFIG.dirs['cmip6']
    
    # Create list of strings representing year column headers
    data_col_headers = ['X{}'.format(i) for i in range(config.CONFIG.ceds_meta['year_first'],
                                                       config.CONFIG.ceds_meta['year_last'] + 1)]
    
    for species in config.CONFIG.freeze_species:
        info_str = '\nCalculating frozen total emissions for {}...'.format(species)
        logger.info(info_str)
        print(info_str)
        
        # Get emission factor file for species
        try:
            frozen_ef_file = ceds_io.get_file_for_species(dir_output, species, "ef")
        except FileNotFoundError as err:
            # If a FileNotFoundError is returned, log it and move on to the next species
            err_str = "Error encountered while fetching EF file: {}".format(err)
            logger.error(err_str)
            failed_species[fail_idx] = species
            fail_idx += 1
            print(err_str)
            continue
        
        # Get activity file for species
        try:
            activity_file = ceds_io.get_file_for_species(dir_cmip6, species, "activity")
        except:
            # If a FileNotFoundError is returned, log it and move on to the next species
            err_msg = 'No activity file found for {}'.format(species)
            logger.error(err_msg)
            failed_species[fail_idx] = species
            fail_idx += 1
            print(err_msg)
            continue
        
        # Read emission factor & activity files into DataFrames
        logger.debug('Reading emission factor file from {}'.format(frozen_ef_file))
        ef_df = pd.read_csv(frozen_ef_file, sep=',', header=0)
        
        logger.debug('Reading activity file from {}'.format(activity_file))
        act_df = pd.read_csv(activity_file, sep=',', header=0)
        
        # Get the 'iso', 'sector', 'fuel', & 'units' columns
        meta_cols = ef_df.iloc[:, 0:4]
        
        # Sanity check
        if (meta_cols.equals(act_df.iloc[:, 0:4])):
            err_str = 'Emission Factor & Activity DataFrames have mis-matched meta columns'
            logger.error(err_str)
            raise ValueError(err_str)
        
        # Get a subset of the emission factor & activity files that contain numerical
        # data so we can compute emissions. We *could* skip this step and just
        # do the slicing whithin the dataframe multiplication step (~line 245),
        # but that is much messier and confusing to read
        logger.debug('Subsetting emission factor & activity DataFrames')
        ef_subs = ef_df[data_col_headers]
        act_subs = act_df[data_col_headers]
        
        logger.debug('Calculating total emissions')
        
        if (ef_subs.shape != act_subs.shape):
            # Error is arising where ef_subs.shape = (55212, 265) &
            # act_subs.shape = (54772, 265).
            # ValueError will be raised by pandas
            logger.error('ValueError: ef_subs & act_subs could not be broadcast together')
            logger.debug('ef_subs.shape {}'.format(ef_subs.shape))
            logger.debug('act_subs.shape {}'.format(act_subs.shape))
        
        emissions_df = pd.DataFrame(ef_subs.values * act_subs.values,
                                    columns=ef_subs.columns, index=ef_subs.index)
        
        # Insert the meta ('iso', 'sector', 'fuel', 'units') columns at the 
        # beginning of the DataFrame
        logger.debug('Concatinating meta_cols and emissions_df DataFrames along axis 1')
        emissions_df = pd.concat([meta_cols, emissions_df], axis=1)
       
        f_name = '{}_total_CEDS_emissions.csv'.format(species)
        
        f_out = os.path.join(dir_output, f_name)
        
        info_str = 'Writing emissions DataFrame to {}'.format(f_out)
        logger.debug(info_str)
        print(info_str + '\n')
        
        emissions_df.to_csv(f_out, sep=',', header=True, index=False)
        logger.info('Finished calculating total emissions for {}'.format(species))
        
    # End species loop
    [logger.warning('Emissions calculation failed for {}'.format(failure))
            for failure in failed_species if failure != '']
    logger.info("Finished processing all species! Leaving validate::calc_emissions()\n")


def main():
    # Create a new argument parser & parse the command line args 
    parser = init_parser()
    args = parser.parse_args()
    
    # Parse the input YAML file & initialize global CONFIG 'constant'
    config.CONFIG = config.ConfigObj(args.input_file)
    
    # Initialize a new main log
    logger = log_config.init_logger('logs', 'main', level='debug')
    logger.info('Input file {}'.format(args.input_file))
    
    info_str = "Function(s) to execute: {}"
    # Execute the specified function(s)
    if (args.function == 'all'):
        func_str = "freeze_emissions() & calc_emissions()"
        logger.info(info_str.format(func_str))
        # --- Func Calls ---
        freeze_emissions()
        calc_emissions()
    elif (args.function == 'freeze_emissions'):
        func_str = "freeze_emissions()"
        logger.info(info_str.format(func_str))
        # --- Func Calls ---
        freeze_emissions()
    elif (args.function == 'calc_emissions'):
        func_str = "calc_emissions()"
        logger.info(info_str.format(func_str))
        # --- Func Calls ---
        calc_emissions()
    else:
        raise ValueError('Invalid function argument. Valid args are "all", "freeze_emissions", or "calc_emissions"')
        


if __name__ == '__main__':
    main()