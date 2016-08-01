"""

some auxiliary stuff here

"""

import os

#clean pdfs folder
def clean_pdfs(filename):
    try:
        if os.path.isfile(filename):
            os.unlink(filename)
    except Exception as e:
        print(e)


