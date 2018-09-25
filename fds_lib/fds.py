# 2018-08-15 david.montaner@gmail.com
# python module for the fds-tools

# FULL CONFIG EXAMPLE

# [local]
# jobname = NAME_OF_THE_JOB
# base_dir_code = /home/dmontaner/code/2017
# base_dir_data = /home/dmontaner/data/2017
# add_jobconf = True
# add_readme = True
# add_gitignore = True
# add_functions_dir = True
# add_script_templates = True

# [tree_code]
# dir_code =
# dir_scripts = scripts
# dir_functions = scripts/functions

# [tree_data]
# dir_data =
# dir_rawdat = data_raw
# dir_proces = data_processed
# dir_res = results/files
# dir_plots = results/plots

# [git]
# gitignore = scripts*/.job.conf
# 	documents/
# 	.DS_Store
# 	__pycache__
# 	.Rhistory

import os
import datetime
import configparser

################################################################################


def infer_jobname_from_path(path=os.getcwd()):
    '''
    The function guesses the jobname from the given path.
    This is the last directory in the path.

    A tuple is returned with component
    - Inferred base_dir_code
    - Inferred name of the job
    '''

    path = path.rstrip(os.sep)
    pathl = path.split(os.sep)

    bdcode = os.sep.join(pathl[:-1])
    jobname = pathl[-1]

    return (bdcode, jobname)


################################################################################


def read_config(file=os.path.join('.fds-tools', 'config'), path=None):
    '''
    Read local fds-tools config file ~/.fds-tools.conf
    '''

    if path is None:
        path = os.path.expanduser('~/')  # this should work for Mac and Linux

    file = os.path.join(path, file)

    config = configparser.ConfigParser()
    config.read_file(open(file))

    conf = {}
    for k in config['local']:
        if k[0:4] == 'add_':
            conf[k] = config['local'].getboolean(k)
        else:
            conf[k] = config['local'][k]

    if 'tree_code' in config.sections():
        # conf['tree_code'] = {k: config['tree_code'][k] for k in config['tree_code']}  # not working in python 2.6
        conf['tree_code'] = {}
        for k in config['tree_code']:
            conf['tree_code'][k] = config['tree_code'][k]

    if 'tree_data' in config.sections():
        # conf['tree_data'] = {k: config['tree_data'][k] for k in config['tree_data']}  # not working in python 2.6
        conf['tree_data'] = {}
        for k in config['tree_data']:
            conf['tree_data'][k] = config['tree_data'][k]

    if 'git' in config.sections():
        conf['gitignore'] = config['git']['gitignore']

    if 'remote' in config.sections():
        # conf['remote'] = {k: config['remote'][k] for k in config['remote']}           # not working in python 2.6
        conf['remote'] = {}
        for k in config['remote']:
            conf['remote'][k] = config['remote'][k]

    return conf

################################################################################


class fdsJob:
    '''
    fds-tools class to store job settings
    '''

    def __init__(
            self,
            jobname=None,
            base_dir_code=None,
            base_dir_data=None,
            email="",
            add_jobconf=True,
            add_readme=True,
            add_gitignore=True,
            add_functions_dir=True,
            add_script_templates=True,
            tree_code=None,
            tree_data=None,
            gitignore=None,
            remote=None
    ):
        '''
        Creates a job settings object (jst) with the local (fds library) settings.
        Use `update_from_conf` to include the user config settings.
        '''

        if tree_code is None:
            tree_code = {
                'dir_code':      "",
                'dir_scripts':   "scripts",
                'dir_functions': os.path.join("scripts", "functions"),
                'dir_docs':      "documents"
            }

        if tree_data is None:
            tree_data = {
                'dir_data':   "",
                'dir_rawdat': "data_raw",
                'dir_proces': "data_processed",
                'dir_res':    os.path.join("results", "files"),
                'dir_plots':  os.path.join("results", "plots"),
            }

        if gitignore is None:
            gitignore = ".DS_Store\n.job.conf\n__pycache__\n.Rhistory\ndocuments/"

        self.jobname = jobname
        self.base_dir_code = base_dir_code
        self.base_dir_data = base_dir_data
        self.email = email
        self.add_jobconf = add_jobconf
        self.add_readme = add_readme
        self.add_gitignore = add_gitignore
        self.add_functions_dir = add_functions_dir
        self.add_script_templates = add_script_templates
        self.tree_code = tree_code
        self.tree_data = tree_data
        self.gitignore = gitignore
        self.remote = remote

    def update_from_conf(self, conf=None):
        '''
        Includes the user config settings into the job settings object (jst).

        There is a little semi BUG in this function:
        It does update the slot when there is new information in the config file.
        But it does not remove the config slot if it disappears from the conf dictionary.
        '''
        if conf is None:
            conf = read_config()

        job_keys = self.__dict__.keys()
        for k in conf.keys():
            if k in job_keys:
                setattr(self, k, conf[k])

    def to_dict(self,
                local=['jobname',
                       'base_dir_code',
                       'base_dir_data',
                       'email',
                       'add_jobconf',
                       'add_readme',
                       'add_gitignore',
                       'add_functions_dir',
                       'add_script_templates'],
                exclude=['jobname']):
        '''
        Converts attributes of the class into a dictionary suitable to be used by configparser.
        - local: a list with the attributes which should go to the "local" section in the dictionary or configparser.
        - exclude: names of attributes which should be excluded. Includes local attributes but also elements in the "tree_code", "tree_data" or "git" sections.
        '''

        # This does not work for python 2.6
        # my_dict = {
        #     'local': {x: getattr(self, x) for x in local if x not in exclude},
        #     'tree_code': {k: v for k, v in self.tree_code.items() if k not in exclude},
        #     'tree_data': {k: v for k, v in self.tree_data.items() if k not in exclude},
        #     'git': {'gitignore': self.gitignore}
        # }

        my_dict = {'local': {},
                    'tree_code': {},
                    'tree_data': {},
                    'git': {}
        }

        for x in local:
            if x not in exclude:
                my_dict['local'][x] = getattr(self, x)

        for k, v in self.tree_code.items():
            if k not in exclude:
                my_dict['tree_code'][k] = v

        for k, v in self.tree_data.items():
            if k not in exclude:
                my_dict['tree_data'][k] = v

        my_dict['git'] = {'gitignore': self.gitignore}

        if self.remote is not None:
            # my_dict['remote'] = {k: v for k, v in self.remote.items() if k not in exclude}  # not working in python 2.6
            my_dict['remote'] = {}
            for k, v in self.remote.items():
                if k not in exclude:
                    my_dict['remote'][k] = v

        return my_dict

    def chek_jobname_not_none(self):
        if self.jobname is None:
            raise Exception('jobname is None. Use jst.jobname = my_name to set it up.')

    def write_job_conf(self, file='.job.conf'):
        '''
        Writes a .job.conf file for a given job.
        '''
        self.chek_jobname_not_none()

        fichero = os.path.join(self.base_dir_code, self.jobname, file)

        dia = datetime.datetime.today().strftime('%Y-%m-%d')

        # header
        lineas = [
            '# ' + file,
            '# ' + dia + ' ' + self.email,
            '# job configuration file',
            # '',
            # '# NOTE: for R and Python Boolean can be replaced by 0,1',
            '',
        ]

        # data paths
        for k, v in self.tree_data.items():
            p = os.path.join(self.base_dir_data, self.jobname, v).rstrip(os.sep)
            l = '{0}="{1}"'.format(k, p)
            lineas.append(l)

        # break
        lineas.append('')

        # code paths
        for k, v in self.tree_code.items():
            p = os.path.join(self.base_dir_code, self.jobname, v).rstrip(os.sep)
            l = '{0}="{1}"'.format(k, p)
            lineas.append(l)

        # end of lines
        lineas = [x + '\n' for x in lineas]

        # SAVE
        f = open(fichero, 'w')
        f.writelines(lineas)
        f.close()

    def write_readme(self, file='README.md'):
        '''
        Writes a README.md file for a given job.
        '''
        self.chek_jobname_not_none()

        fichero = os.path.join(self.base_dir_code, self.jobname, file)

        lineas = [self.jobname, '=' * 80]
        lineas = [x + '\n' for x in lineas]

        f = open(fichero, 'w')
        f.writelines(lineas)
        f.close()

    def write_gitignore(self, file='.gitignore'):
        '''
        Writes a .gitignore file for a given job.
        '''
        self.chek_jobname_not_none()

        fichero = os.path.join(self.base_dir_code, self.jobname, file)

        lineas = self.gitignore
        lineas = lineas + '\n'
        # lineas = [x + '\n' for x in lineas]

        f = open(fichero, 'w')
        f.writelines(lineas)
        f.close()

    def exists_dir_data(self):
        '''
        Tests if a data directory exist with the given job.
        Returns True or False.
        '''
        self.chek_jobname_not_none()
        d = os.path.join(self.base_dir_data, self.jobname)
        e = os.path.isdir(d) | os.path.isfile(d)
        return e

    def exists_dir_code(self):
        '''
        Tests if a code directory exist with the given job.
        Returns True or False.
        '''
        self.chek_jobname_not_none()
        d = os.path.join(self.base_dir_code, self.jobname)
        e = os.path.isdir(d) | os.path.isfile(d)
        return e

    def exist_job_conf(self, file='.job.conf'):
        '''
        Tests if a .job.conf file exist for the given job.
        Returns True or False.
        '''
        self.chek_jobname_not_none()
        d = os.path.join(self.base_dir_code, self.jobname, self.tree_code['dir_scripts'], file)
        e = os.path.isdir(d) | os.path.isfile(d)
        return e

    def create_dir_data(self):
        '''
        Creates a data template directory for the given job.
        No warning or error is given if the directory exists.
        But if it exists and has content nothing is deleted or lost.
        '''
        self.chek_jobname_not_none()

        for v in self.tree_data.values():
            d = os.path.join(self.base_dir_data, self.jobname, v).rstrip(os.sep)
            # os.makedirs(d, exist_ok=True)  # not working in python 2.6
            try:
                os.makedirs(d)
            except:
                pass

    def create_dir_code(self):
        '''
        Creates a dir template directory for the given job.
        No warning or error is given if the directory exists.
        But if it exists and has content nothing is deleted or lost.
        Other files such as README.md of .job.conf are not created by this method.
        '''
        self.chek_jobname_not_none()

        # DEAL WITH THE FUNCTIONS DIRECTORY
        if not self.add_functions_dir:
            self.tree_code.pop('dir_functions')

        for v in self.tree_code.values():
            d = os.path.join(self.base_dir_code, self.jobname, v).rstrip(os.sep)
            # os.makedirs(d, exist_ok=True)  # not working in python 2.6
            try:
                os.makedirs(d)
            except:
                pass

    def create_job(self):
        '''
        Creates code and data directories for a new job.
        The function returns an error and stops if any of the two directories already exists.
        '''
        # To Do:
        # implement
        # - 'add_script_templates'
        self.chek_jobname_not_none()

        code_dir = os.path.join(self.base_dir_code, self.jobname)
        data_dir = os.path.join(self.base_dir_data, self.jobname)

        # TEST IF THE DIRECTORIES EXIST
        code_dir_exists = self.exists_dir_code()
        data_dir_exists = self.exists_dir_data()

        if code_dir_exists:
            print('Code directory "' + code_dir + '" already exists')

        if data_dir_exists:
            print('Data directory "' + data_dir + '" already exists')

        if code_dir_exists | data_dir_exists:
            # exit(1) # this seems to be good for scripts but not for functions
            raise Exception('job already exists')

        # CREATE NEW FOLDERS
        print('Creating folders:')

        print(code_dir)
        self.create_dir_code()

        print(data_dir)
        self.create_dir_data()

        # CREATE EXTRA FILES
        # All these will overwrite the files.
        # It should not matter as the job is new and files should not exist.

        if self.add_jobconf:
            self.write_job_conf()

        if self.add_readme:
            self.write_readme()

        if self.add_gitignore:
            self.write_gitignore()

        # COPY TEMPLATES
        # implement here
