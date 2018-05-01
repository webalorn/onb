import onb, env.production.settings
from api.api import *
import onb
from sqldb.db import *

generateStructure(verbose=True)

application = onb.app