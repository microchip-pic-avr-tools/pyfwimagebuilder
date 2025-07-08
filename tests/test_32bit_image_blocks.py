"""
Unit tests for image block encoding/decoding for MCU32 file format.
"""
import unittest
from pathlib import Path
import pytest
from pyfwimagebuilder.mcu32builder import MetaDataBlock, FlashWriteBlock, BlockType

DATA_FOLDER = Path(__file__).parent.absolute() / 'data' / 'MCU32'

class TestImageBlocks(unittest.TestCase):
    """Test basic encoding and decoding of image blocks
    """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        with open(DATA_FOLDER / "v1.0.0/PIC32_TestApp.image", "rb") as imagefile:
            self.metablock_bytes = imagefile.read(0x47)
            self.flashblock_bytes = imagefile.read(0x47)

    def test_metadata_block(self):
        """Test decoding and encoding of a metadata block
        """

        # Test decoding and encoding of metadata block
        metadata_block = MetaDataBlock.from_bytes(self.metablock_bytes)
        tmp = metadata_block.to_bytes()
        self.assertEqual(self.metablock_bytes, tmp)

        # Test detection of invalid block size
        tmp = bytearray(self.metablock_bytes)
        tmp[0] = 0 # Set size that does not match actual object size
        with pytest.raises(ValueError):
            MetaDataBlock.from_bytes(tmp)

        # Test detection of invalid block type
        tmp = bytearray(self.metablock_bytes)
        tmp[2] = 5 # Set invalid block type
        with pytest.raises(ValueError):
            MetaDataBlock.from_bytes(tmp)

    def test_flashwrite_block(self):
        """Test decoding and encoding of flash write operation block
        """
        # Test decoding and encoding of flash write block
        flashblock = FlashWriteBlock.from_bytes(self.flashblock_bytes)
        tmp =flashblock.to_bytes()
        self.assertEqual(tmp, self.flashblock_bytes)

        # Test detection of invalid block size
        tmp = bytearray(self.metablock_bytes)
        tmp[0] = 0 # Set size that does not match actual object size
        with pytest.raises(ValueError):
            FlashWriteBlock.from_bytes(tmp)

        # Test detection of invalid block type
        tmp = bytearray(self.metablock_bytes)
        tmp[2] = BlockType.METADATA.value # Set metadata block type instead of flash write block type
        with pytest.raises(ValueError):
            FlashWriteBlock.from_bytes(tmp)
