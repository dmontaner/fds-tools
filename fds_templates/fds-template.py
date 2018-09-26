# (>>>FILE<<<)
# (>>>ISO_DATE<<<) (>>>EMAIL<<<)
# (>>>COMMENT<<<)

import os
# import sys
# import re
# import time
# import shutil
# import numpy as np
import pandas as pd
# import sklearn as sk
# from scipy import stats
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns
# import feather
# import json
# import pickle

# CONFIGURATION
try:
    try:
        from importlib.machinery import SourceFileLoader
        _job = SourceFileLoader('job_config', '../.job.conf').load_module()
        print('config imported using: importlib')
    except:
        from imp import load_source
        _job = load_source('job_config', '../.job.conf')
        print('config imported using: imp')
except:
    pass

# # FUNCTIONS
# try:
#     mymod = SourceFileLoader('mod', os.path.join(_job.dir_functions, 'mymod.py')).load_module()
#     print('functions imported using: importlib')
# except:
#     mymod = load_source('mod', os.path.join(_job.dir_functions, 'mymod.py'))
#     print('functions imported using: imp')

pd.set_option('display.width', 173)
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)
# pd.set_option('display.max_colwidth', 100)
# pd.get_option('display.expand_frame_repr')

# np.set_printoptions(linewidth=240)

# plt.style.use('ggplot')
# matplotlib.rc('figure', figsize=[20, 20])
# matplotlib.rc('figure', figsize=[40, 20], dpi=200)
# matplotlib.rc('font', size=20)

################################################################################

# DATA
os.chdir(_job.dir_rawdat)
os.chdir(_job.dir_proces)
os.chdir(_job.dir_res)
os.chdir(_job.dir_plots)

os.path.join(_job.dir_proces, 'MY', 'PATH', 'TO', 'FILE.TXT')
os.listdir()

datos = pd.read_table('')
datos.shape
datos.dtypes.value_counts()
datos.head()


# LOOPS
for fi in os.listdir(_job.dir_rawdat):
    print('\n\n==========', fi, '==========\n')


# SAVE
os.chdir(_job.dir_proces)

datos.to_feather('datos.feather')
datos.reset_index().to_feather('datos.feather')
feather.write_dataframe(datos, 'datos.feather')

datos.to_pickle('datos.pkl', compression=None)
datos.to_pickle('datos.pkl.gz', compression='gzip')  # slow

datos.to_csv('datos.csv.gz')
datos.to_csv('datos.tsv.gz', sep='\t')


# PLOTS
plt.close('all')
# YOUR POLOT HERE
plt.show(block=False)
#
plt.savefig('PLOT_NAME.png')
plt.close()


# EXIT
print('\nPython SUCCESSFULLY finished')
