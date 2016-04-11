import os

home_dir = os.environ['HOME']

if os.path.isdir("$HOME/.ipython/profile_nbserver")is False:
    os.system("ipython profile create nbserver")
else: 
    os.system("echo profile_nbserver is already exist.")

from IPython.lib import passwd
pwsha = passwd()
   
config_str = """
# Server config
c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.password = u'{}'
# It is a good idea to put it on a known, fixed port
c.NotebookApp.port = 8888
c.NotebookApp.notebook_dir = u'/'
""".format(pwsha)

with open(home_dir+"/.ipython/profile_nbserver/ipython_notebook_config.py", "w") as cf:
    cf.write(config_str)
        

#os.system("sudo printf \"\nexport PATH=/usr/local/cuda/bin:$PATH\nexport LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH\n\" >> /root/.bashrc")
#os.system("sudo printf \"\nshell -/bin/bash\n\" >> /root/.screenrc")

# this is usually make some error... do not use this!
#os.system("screen -dRR -dmS ipython_notebook ipython notebook --profile=nbserver;")

# https://www.gnu.org/software/screen/manual/screen.html
# screen install check
# 
