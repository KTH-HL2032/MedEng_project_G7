from src.niryo_prc.niryocore import NiryoCore
from oBCI_prc.obcicore import *


def run():
    niryocore_instance = NiryoCore()
    n = niryocore_instance.niryo_connect()

    obcicore_instance = ObciCore()
    p = obcicore_instance.processing()


    while True:
        return 0



if __name__ == '__main__':
    run()




