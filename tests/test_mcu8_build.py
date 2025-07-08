"""
Tests releated to mcu8builder module
"""
import unittest
import os
import io
from pathlib import Path
import toml
from mock import patch
import intelhex
from pyfwimagebuilder.mcu8builder import FirmwareImageBuilderMcu8, Mcu8FirmwareImage
from pyfwimagebuilder.builder import builder_factory

pic18f_v3_test_config = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'data','MCU8','v0.3.0', 'configs',
                                     'bootloader_config_pic18.toml')

DATA_FOLDER = Path(__file__).parent.absolute() / 'data' / 'MCU8'

class TestMcu8BuilderPic18(unittest.TestCase):
    """
    Testing FirmwareImageBuilderMcu8 for PIC18 parts
    """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = toml.load(pic18f_v3_test_config)

    def _mock_stdout(self):
        """
        Returns stdout mock.

        Content sent to stdout can be fetched with mock_stdout.getvalue()
        """
        mock_stdout_patch = patch('sys.stdout', new_callable=io.StringIO)
        self.addCleanup(mock_stdout_patch.stop)
        return mock_stdout_patch.start()

    def _mock_stderr(self):
        """
        Returns stderr mock.

        Content sent to stderr can be fetched with mock_stderr.getvalue()
        """
        mock_stderr_patch = patch('sys.stderr', new_callable=io.StringIO)
        self.addCleanup(mock_stderr_patch.stop)
        return mock_stderr_patch.start()

    def test_versiontobytes(self):
        """Test converting version string to bytes
        """
        mcu8_builder = FirmwareImageBuilderMcu8(self.config, Mcu8FirmwareImage)
        min_version = mcu8_builder.versiontobytes(mcu8_builder.MIN_FORMAT_VERSION)
        max_version = mcu8_builder.versiontobytes(mcu8_builder.MAX_FORMAT_VERSION)
        self.assertEqual(max_version, bytes([0,3,0]), "versiontobytes Failed.")
        self.assertEqual(min_version, bytes([0,3,0]), "versiontobytes Failed.")

    def test_is_valid_version(self):
        """Test the version validator
        """
        mcu8_builder = FirmwareImageBuilderMcu8(self.config, Mcu8FirmwareImage)
        current_version = self.config['bootloader']['IMAGE_FORMAT_VERSION']
        self.assertTrue((mcu8_builder.is_valid_version(current_version)),"Version Check Failed.")
        self.assertTrue((mcu8_builder.is_valid_version("0.3.0")),"Version Check Failed.")
        self.assertFalse((mcu8_builder.is_valid_version("0.4.0")),"Version Check Failed.")
        self.assertFalse((mcu8_builder.is_valid_version("0.2.0")),"Version Check Failed.")
        self.assertFalse((mcu8_builder.is_valid_version("1.0.0")),"Version Check Failed.")

        # The versions are class variables so these will live as long as the program executes
        # That means we need to store version so that we can restore it afterwards
        tmp_min_version = FirmwareImageBuilderMcu8.MIN_FORMAT_VERSION
        tmp_max_version = FirmwareImageBuilderMcu8.MAX_FORMAT_VERSION
        FirmwareImageBuilderMcu8.MIN_FORMAT_VERSION = "0.3.0"
        FirmwareImageBuilderMcu8.MAX_FORMAT_VERSION = "1.0.0"
        self.assertTrue((mcu8_builder.is_valid_version(current_version)),"Version Check Failed.")
        self.assertTrue((mcu8_builder.is_valid_version("1.0.0")),"Version Check Failed.")
        self.assertTrue((mcu8_builder.is_valid_version("0.3.0")),"Version Check Failed.")
        self.assertTrue((mcu8_builder.is_valid_version("0.4.0")),"Version Check Failed.")
        # Set version back
        FirmwareImageBuilderMcu8.MIN_FORMAT_VERSION = tmp_min_version
        FirmwareImageBuilderMcu8.MAX_FORMAT_VERSION = tmp_max_version

    @patch('logging.Logger._log')
    def test_data_outside_segment(self, mock_log):
        """Test that data from hexfile that is outside of a defined memory area is skipped.
        """
        hexfile = DATA_FOLDER / 'applications' / 'PIC18F57Q43_App_checksum.hex'

        ihex= intelhex.IntelHex()
        ihex.fromfile(hexfile, format="hex")
        # Add some data after the flash memory area into the hexfile
        segment_start = self.config["bootloader"]["FLASH_END"] + 1
        ihex[segment_start] = 0xaa

        architecture = self.config['bootloader']['ARCH']
        builder = builder_factory(architecture, self.config)
        builder.build(ihex, include_empty_blocks=False)
        expected_message = f"Skipping segment from 0x{segment_start:08X}"
        log_messages = [call[0][1] for call in mock_log.call_args_list]
        self.assertTrue(any(expected_message in message for message in log_messages))
