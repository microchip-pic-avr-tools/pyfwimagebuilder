"""
Integration tests using the pyfwimagebuilder CLI
"""
import unittest
import sys
import io
import tempfile
from pathlib import Path
import pytest
from mock import patch
from pyfwimagebuilder import __version__ as VERSION
from pyfwimagebuilder import BUILD_DATE

from pyfwimagebuilder.pyfwimagebuilder import main

DATA_FOLDER = Path(__file__).parent.absolute() / 'data'

class TestPyfwimagebuilder(unittest.TestCase):
    """Integration tests for pyfwimagebuilder
    """
    def _mock_stdout(self):
        """
        Returns stdout mock.

        Content sent to stdout can be fetched with mock_stdout.getvalue()
        """
        mock_stdout_patch = patch('sys.stdout', new_callable=io.StringIO)
        self.addCleanup(mock_stdout_patch.stop)
        return mock_stdout_patch.start()

    def _generate_and_verify_image(self, appfile, configfile, referencefile):
        """Generate image and compare with reference image

        Uses the pyfwimagebuilder CLI to generate an image for the provided application file and compare it to the
        provided reference image
        :param appfile: Application file (hex file) to use as basis for generated image
        :type appfile: class:`pathlib.Path`
        :param configfile: Configuration file to use when generating image
        :type configfile: class:'pathlib.Path'
        :param referencefile: What the generated image is expected to be
        :type referencefile: class:'pathlib.Path'
        """
        with tempfile.TemporaryDirectory() as tempdir:
            outputfile = Path(tempdir) / 'generated.image'

            testargs = ["pyfwimagebuilder", "build", "-i", str(appfile), "-c", str(configfile), "-o", str(outputfile)]
            with patch.object(sys, 'argv', testargs):
                retval = main()
            self.assertEqual(retval, 0)

            with referencefile.open('rb') as ref:
                with outputfile.open('rb') as out:
                    ref_hex = ref.read().hex()
                    out_hex = out.read().hex()
                    # The maxDiff attribute is part of unittest so nothing we can do about its name
                    # pylint: disable=invalid-name
                    self.maxDiff = None
                    self.assertEqual(out_hex, ref_hex, msg="Generated image does not match expected image")

    def _decode_and_verify(self, imagefile, referencefile, configfile):
        """Decode image and compare with reference image

        Uses the pyfwimagebuilder CLI to decode an image for the provided application file and compare it to the
        provided reference image
        :param imagefile: Image file for decoding
        :type imagefile: class:`pathlib.Path`
        :param configfile: Configuration file to use when decoding image
        :type configfile: class:'pathlib.Path'
        :param referencefile: What the decoded image test is expected to be
        :type referencefile: class:'pathlib.Path'
        """
        with tempfile.TemporaryDirectory() as tempdir:
            outputfile = Path(tempdir) / 'generated.image'

            testargs = ["pyfwimagebuilder", "decode", "-i", str(imagefile), "-o", str(outputfile), "-c", str(configfile)]
            with patch.object(sys, 'argv', testargs):
                retval = main()
            self.assertEqual(retval, 0)

            with referencefile.open('r') as ref:
                with outputfile.open('r') as out:
                    ref = ref.read()
                    out = out.read()
                    # The maxDiff attribute is part of unittest so nothing we can do about its name
                    # pylint: disable=invalid-name
                    self.maxDiff = None
                    self.assertEqual(out, ref, msg="Decoded image does not match expected image")

    def test_pic18_v0_3_0_image(self):
        """
        Test generating image version 0.3.0 for PIC18
        """
        appfile = DATA_FOLDER / 'MCU8' / 'applications' / 'PIC18F57Q43_App_checksum.hex'
        configfile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'configs' / 'bootloader_config_pic18.toml'
        referencefile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'PIC18F57Q43_App_checksum_v0_3_0.image'

        self._generate_and_verify_image(appfile, configfile, referencefile)

    def test_pic16_v0_3_0_image(self):
        """
        Test generating image version 0.3.0 for PIC16
        """
        appfile = DATA_FOLDER / 'MCU8' / 'applications' / 'PIC16F18875_App_checksum.hex'
        configfile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'configs' / 'bootloader_config_pic16.toml'
        referencefile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'PIC16F18875_App_checksum_v0_3_0.image'

        self._generate_and_verify_image(appfile, configfile, referencefile)

    def test_avr_v0_3_0_image(self):
        """
        Test generating image version 0.3.0 for AVR
        """
        appfile = DATA_FOLDER / 'MCU8' / 'applications' / 'AVR128DA48_App_checksum.hex'
        configfile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'configs' / 'bootloader_config_avr.toml'
        referencefile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'AVR128DA48_App_checksum_v0_3_0.image'

        self._generate_and_verify_image(appfile, configfile, referencefile)

    def test_pic32_v1_0_0_image(self):
        """
        Test generating image version 1.0.0 for MCU32 devices
        """
        appfile = DATA_FOLDER / 'MCU32' / 'applications' / 'PIC32_TestApp.X.production.hex'
        configfile = DATA_FOLDER / 'MCU32' / 'v1.0.0' / 'configs' / 'bootloader_config_pic32cm.toml'
        referencefile = DATA_FOLDER / 'MCU32' / 'v1.0.0' / 'PIC32_TestApp.image'

        self._generate_and_verify_image(appfile, configfile, referencefile)

    def test_decoding_avr_v0_3_0_image(self):
        """
        Test decoding image version 0.3.0 for AVR
        """
        imagefile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'AVR128DA48_App_checksum_v0_3_0.image'
        referencefile = DATA_FOLDER / 'MCU8' / 'v0.3.0/decoded' / 'AVR128DA48_App_checksum_v0_3_0.image.txt'
        configfile = DATA_FOLDER / 'MCU8' / 'v0.3.0/configs' / 'bootloader_config_avr.toml'

        self._decode_and_verify(imagefile, referencefile, configfile)

    def test_decoding_pic18_v0_3_0_image(self):
        """
        Test decoding image version 0.3.0 for PIC18
        """
        imagefile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'PIC18F57Q43_App_checksum_v0_3_0.image'
        referencefile = DATA_FOLDER / 'MCU8' / 'v0.3.0/decoded' / 'PIC18F57Q43_App_checksum_v0_3_0.image.txt'
        configfile = DATA_FOLDER / 'MCU8' / 'v0.3.0/configs' / 'bootloader_config_pic18.toml'

        self._decode_and_verify(imagefile, referencefile, configfile)

    def test_decoding_pic16_v0_3_0_image(self):
        """
        Test decoding image version 0.3.0 for PIC16
        """
        imagefile = DATA_FOLDER / 'MCU8' / 'v0.3.0' / 'PIC16F18875_App_checksum_v0_3_0.image'
        referencefile = DATA_FOLDER / 'MCU8' / 'v0.3.0/decoded' / 'PIC16F18875_App_checksum_v0_3_0.image.txt'
        configfile = DATA_FOLDER / 'MCU8' / 'v0.3.0/configs' / 'bootloader_config_pic16.toml'

        self._decode_and_verify(imagefile, referencefile, configfile)

    def test_decoding_pic32_v1_0_0_image(self):
        """
        Test decoding image version 1.0.0 for MCU32 devices
        """
        imagefile = DATA_FOLDER / 'MCU32' / 'v1.0.0' / 'PIC32_TestApp.image'
        referencefile = DATA_FOLDER / 'MCU32' / 'v1.0.0' / 'decoded' / 'PIC32_TestApp.image.txt'
        configfile = DATA_FOLDER / 'MCU32' / 'v1.0.0' / 'configs' / 'bootloader_config_pic32cm.toml'

        self._decode_and_verify(imagefile, referencefile, configfile)

    def test_decode_cmd_help(self):
        """Test CLI help for decode action
        """
        mock_stdout = self._mock_stdout()
        testargs = ["pyfwimagebuilder", "decode", "--help"]
        with patch.object(sys, 'argv', testargs):
            with pytest.raises(SystemExit) as e:
                main()
            self.assertEqual(e.type, SystemExit)
            self.assertEqual(e.value.code, 0)
        self.assertIn("usage: pyfwimagebuilder decode", mock_stdout.getvalue())

    def test_get_version(self):
        """Test that pyfwimagebuilder CLI returns a version"""
        mock_stdout = self._mock_stdout()
        testargs = ["pyfwimagebuilder", "--version"]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        self.assertIn(f'pyfwimagebuilder version {VERSION}', mock_stdout.getvalue())

        testargs = ["pyfwimagebuilder", "-V"]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        self.assertIn(f'pyfwimagebuilder version {VERSION}', mock_stdout.getvalue())

    def test_get_release_info(self):
        """Test that pyfwimagebuilder CLI returns the release info"""
        mock_stdout = self._mock_stdout()
        testargs = ["pyfwimagebuilder", "--release-info"]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        self.assertIn(f"pyfwimagebuilder version {VERSION}", mock_stdout.getvalue())
        self.assertIn(f"Build date:  {BUILD_DATE}", mock_stdout.getvalue())

        testargs = ["pyfwimagebuilder", "-R"]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        self.assertIn(f"pyfwimagebuilder version {VERSION}", mock_stdout.getvalue())
        self.assertIn(f"Build date:  {BUILD_DATE}", mock_stdout.getvalue())
