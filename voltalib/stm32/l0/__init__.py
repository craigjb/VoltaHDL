import os.path

from voltahdl import C

from ..base import STM32Component, generate_stm32_component


class STM32L0Component(STM32Component):
    def __init__(self):
        super().__init__()

    def decouple_vdd(self):
        """
        Generates decoupling capacitors for the VDD rail per ST recommendations

        Follows page 11 at:
        https://www.st.com/content/ccc/resource/technical/document/application_note/fd/f4/6b/40/9a/b5/41/a2/DM00112257.pdf/files/DM00112257.pdf/jcr:content/translations/en.DM00112257.pdf
        """
        self.pins.VDD > C('10 uF') < self.pins.VSS
        if isinstance(self.pins.VDD.number, list):
            for _ in range(len(self.pins.VDD.number)):
                self.pins.VDD > C('100 nF') < self.pins.VSS
        else:
            self.pins.VDD > C('100 nF') < self.pins.VSS


STM32L073RZ = generate_stm32_component(
    'STM32L073RZ', STM32L0Component,
    os.path.join(os.path.dirname(__file__), 'STM32L073RZ.csv'),
    'https://www.st.com/resource/en/datasheet/stm32l073rz.pdf'
)

STM32L011x3 = generate_stm32_component(
    'STM32L011x3', STM32L0Component,
    os.path.join(os.path.dirname(__file__), 'STM32L011x3_4.csv'),
    'https://www.st.com/resource/en/datasheet/stm32l011d4.pdf'
)

STM32L011x4 = generate_stm32_component(
    'STM32L011x4', STM32L0Component,
    os.path.join(os.path.dirname(__file__), 'STM32L011x3_4.csv'),
    'https://www.st.com/resource/en/datasheet/stm32l011d4.pdf'
)
