import os.path

from ..base import generate_stm32_component


STM32L073RZ = generate_stm32_component(
    'STM32L073RZ',
    os.path.join(os.path.dirname(__file__), 'STM32L073RZ.csv')
)

STM32L011x3 = generate_stm32_component(
    'STM32L011x3',
    os.path.join(os.path.dirname(__file__), 'STM32L011x3_4.csv')
)

STM32L011x4 = generate_stm32_component(
    'STM32L011x4',
    os.path.join(os.path.dirname(__file__), 'STM32L011x3_4.csv')
)
