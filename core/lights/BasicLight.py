import numpy as np
class Light:
    def __init__(self):
        self.pos = np.zeros(4)
        self.normal = np.zeros(4)
        self.normal[3] = 1

        self.custom_script = False #Custom lighting scripts could be implemented to allow for more accurate lighting