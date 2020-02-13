"""
This file holds variables and whatnot for use in tests

Matt Nicholson
12 Feb 2020
"""
# CMIP6/CEDS combustion-related sectors 
expected_sectors = sorted(
    ['1A1a_Electricity-public', '1A1a_Electricity-autoproducer',
     '1A1a_Heat-production', '1A2a_Ind-Comb-Iron-steel', '1A2b_Ind-Comb-Non-ferrous-metals',
     '1A2c_Ind-Comb-Chemicals', '1A2d_Ind-Comb-Pulp-paper', '1A2e_Ind-Comb-Food-tobacco',
     '1A2f_Ind-Comb-Non-metalic-minerals', '1A2g_Ind-Comb-Construction',
     '1A2g_Ind-Comb-transpequip', '1A2g_Ind-Comb-machinery', '1A2g_Ind-Comb-mining-quarying',
     '1A2g_Ind-Comb-wood-products', '1A2g_Ind-Comb-textile-leather', '1A2g_Ind-Comb-other',
     '1A3ai_International-aviation', '1A3aii_Domestic-aviation', '1A3b_Road',
     '1A3c_Rail', '1A3di_International-shipping', '1A3dii_Domestic-navigation',
     '1A3eii_Other-transp', '1A4a_Commercial-institutional', '1A4b_Residential',
     '1A4c_Agriculture-forestry-fishing', '1A5_Other-unspecified']
    )
            
# CMIP6/CEDS fuels          
expected_fuels = sorted(
    ['biomass', 'brown_coal', 'coal_coke', 'diesel_oil',
     'hard_coal', 'heavy_oil', 'light_oil', 'natural_gas']
    )

# CMIP6/CEDS ISOs                   
expected_isos = sorted(
    ['abw', 'afg', 'ago', 'alb', 'are', 'arg', 'arm', 'asm',
     'atg', 'aus', 'aut', 'aze', 'bdi', 'bel', 'ben', 'bfa', 'bgd', 'bgr',
     'bhr', 'bhs', 'bih', 'blr', 'blz', 'bmu', 'bol', 'bra', 'brb', 'brn',
     'btn', 'bwa', 'caf', 'can', 'che', 'chl', 'chn', 'civ', 'cmr', 'cod',
     'cog', 'cok', 'col', 'com', 'cpv', 'cri', 'cub', 'cuw', 'cym', 'cyp',
     'cze', 'deu', 'dji', 'dma', 'dnk', 'dom', 'dza', 'ecu', 'egy', 'eri',
     'esh', 'esp', 'est', 'eth', 'fin', 'fji', 'flk', 'fra', 'fro', 'fsm',
     'gab', 'gbr', 'geo', 'gha', 'gib', 'gin', 'global', 'glp', 'gmb', 'gnb',
     'gnq', 'grc', 'grd', 'grl', 'gtm', 'guf', 'gum', 'guy', 'hkg', 'hnd',
     'hrv', 'hti', 'hun', 'idn', 'ind', 'irl', 'irn', 'irq', 'isl', 'isr',
     'ita', 'jam', 'jor', 'jpn', 'kaz', 'ken', 'kgz', 'khm', 'kir', 'kna',
     'kor', 'kwt', 'lao', 'lbn', 'lbr', 'lby', 'lca', 'lie', 'lka', 'lso',
     'ltu', 'lux', 'lva', 'mac', 'mar', 'mda', 'mdg', 'mdv', 'mex', 'mhl',
     'mkd', 'mli', 'mlt', 'mmr', 'mne', 'mng', 'moz', 'mrt', 'msr', 'mtq',
     'mus', 'mwi', 'mys', 'nam', 'ncl', 'ner', 'nga', 'nic', 'niu', 'nld',
     'nor', 'npl', 'nzl', 'omn', 'pak', 'pan', 'per', 'phl', 'plw', 'png',
     'pol', 'pri', 'prk', 'prt', 'pry', 'pse', 'pyf', 'qat', 'reu', 'rou',
     'rus', 'rwa', 'sau', 'sdn', 'sen', 'sgp', 'slb', 'sle', 'slv', 'som',
     'spm', 'srb', 'srb (kosovo)', 'ssd', 'stp', 'sur', 'svk', 'svn', 'swe',
     'swz', 'sxm', 'syc', 'syr', 'tca', 'tcd', 'tgo', 'tha', 'tjk', 'tkl',
     'tkm', 'tls', 'ton', 'tto', 'tun', 'tur', 'twn', 'tza', 'uga', 'ukr',
     'ury', 'usa', 'uzb', 'vct', 'ven', 'vgb', 'vir', 'vnm', 'vut', 'wlf',
     'wsm', 'yem', 'zaf', 'zmb', 'zwe']
    )
    
# Non-combustion sectors
non_combustion_sectors = sorted(
    ['1A1bc_Other-transformation', '1A1bc_Other-feedstocks', '1B1_Fugitive-solid-fuels',
     '1B2_Fugitive-petr-and-gas', '1B2d_Fugitive-other-energy', '2A1_Cement-production',
     '2A2_Lime-production', '2A6_Other-minerals', '2B_Chemical-industry', '2C_Metal-production',
     '2D_Degreasing-Cleaning', '2D3_Other-product-use', '2D_Paint-application',
     '2D3_Chemical-products-manufacture-processing', '2H_Pulp-and-paper-food-beverage-wood',
     '2L_Other-process-emissions', '3B_Manure-management', '3D_Soil-emissions',
     '3I_Agriculture-other', '3D_Rice-Cultivation', '3E_Enteric-fermentation',
     '3F_Agricultural-residue-burning-on-fields', '5A_Solid-waste-disposal',
     '5E_Other-waste-handling', '5C_Waste-incineration', '6A_Other-in-total',
     '5D_Wastewater-handling', '6B_Other-not-in-total', '7A_Fossil-fuel-fires',
     '11A_Volcanoes', '11B_Forest-fires', '11C_Other-natural']
    )
    
def subset_df(ef_df, iso):
    df = ef_df.loc[(ef_df['iso'] == iso) &
                   (ef_df['sector'].isin(expected_sectors))]
    return df