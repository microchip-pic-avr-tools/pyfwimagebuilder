import unittest
import toml
import os
from pyfwimagebuilder.mcu32builder import FirmwareImageBuilderMcu32, Mcu32FirmwareImage

pic32cm_v3_test_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','MCU32','v1.0.0', 'configs', 'bootloader_config_pic32cm.toml')

class TestMcu32Builder_default(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = toml.load(pic32cm_v3_test_config)

    def test_versiontobytes(self):
        mcu_builder = FirmwareImageBuilderMcu32(self.config, Mcu32FirmwareImage)
        min_version = mcu_builder.versiontobytes(mcu_builder.MIN_FORMAT_VERSION)
        max_version = mcu_builder.versiontobytes(mcu_builder.MAX_FORMAT_VERSION)
        # Versions are returned in little endian
        self.assertEqual(max_version, bytes([0,0,1]), "versiontobytes Failed.")
        self.assertEqual(min_version, bytes([0,0,1]), "versiontobytes Failed.")

    def test_is_valid_version(self):
        mcu_builder = FirmwareImageBuilderMcu32(self.config, Mcu32FirmwareImage)
        current_version = self.config['bootloader']['IMAGE_FORMAT_VERSION']
        self.assertTrue((mcu_builder.is_valid_version(current_version)),"Version Check Failed.")
        self.assertFalse((mcu_builder.is_valid_version("0.2.0")),"Version Check Failed.")
        self.assertFalse((mcu_builder.is_valid_version("1.1.0")),"Version Check Failed.")
