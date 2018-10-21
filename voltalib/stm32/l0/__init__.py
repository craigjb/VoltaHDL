import os.path

from voltahdl import *
from ..pinout import STM32Pinout

PINOUT_DIR = os.path.dirname(__file__)

STM32L0 = def_component_series('STM32L0')


@STM32L0.def_helper
def decouple_vdd(c):
    """
    Generates decoupling capacitors for the VDD rail per ST recommendations
    Follows page 11 at:
    https://www.st.com/content/ccc/resource/technical/document/application_note/fd/f4/6b/40/9a/b5/41/a2/DM00112257.pdf/files/DM00112257.pdf/jcr:content/translations/en.DM00112257.pdf
    """
    c.pins.VDD > C('10 uF') < c.pins.VSS
    if isinstance(c.pins.VDD.number, list):
        for _ in range(len(c.pins.VDD.number)):
            c.pins.VDD > C('100 nF') < c.pins.VSS
    else:
        c.pins.VDD > C('100 nF') < c.pins.VSS


STM32L073xx = def_component(
    'STM32L073xx', 'U',
    series=STM32L0,
    datasheet='https://www.st.com/resource/en/datasheet/stm32l073rz.pdf',
    pinout=STM32Pinout(os.path.join(PINOUT_DIR, 'STM32L073RZ.csv'))
)


STM32L011x3 = def_component(
    'STM32L011x3', 'U',
    series=STM32L0,
    datasheet='https://www.st.com/resource/en/datasheet/stm32l011d4.pdf',
    pinout=STM32Pinout(os.path.join(PINOUT_DIR, 'STM32L011x3_4.csv'))
)

STM32L011x4 = def_component(
    'STM32L011x4', 'U',
    series=STM32L0,
    datasheet='https://www.st.com/resource/en/datasheet/stm32l011d4.pdf',
    pinout=STM32Pinout(os.path.join(PINOUT_DIR, 'STM32L011x3_4.csv'))
)
