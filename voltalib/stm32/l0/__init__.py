import os.path

from ..base import STM32Component, generate_stm32_component


class STM32L0Component(STM32Component):
    def __init__(self):
        super().__init__()


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
