import sys
from imp import reload

reload(sys)
import os
envPath = os.getenv('TOOLBOX')
toolPath = envPath + '/Libs'
sys.path.append(toolPath)
# import userinterface
# reload(userinterface)

from Libs.ui import RefreshWindow as refresh

reload(refresh)
rw =refresh.RefreshWindow
rw.refresh_window(rw)


