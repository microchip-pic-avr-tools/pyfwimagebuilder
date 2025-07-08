# pyfwimagebuilder - Firmware Image Builder
pyfwimagebuilder is a tool and library for building firmware update images for Microchip microcontrollers

# Usage
pyfwimagebuilder is used as a command line interface:

```
pyfwimagebuilder [switches]
```

## Mandatory arguments
```
-i, --input
    Input file to process (in Intel-hex format)

-c, --config
    Configuration file to use when processing
```

## Optional arguments
```
-o, --output
    Output file to generate.
    If not supplied, the input filename will be used with .img extension
```    

## Additional arguments and switches
```
-h, --help
    Show this help message and exit

-V, --version
    Print pyfwimagebuilder version number and exit

-R, --release-info
    Print pyfwimagebuilder release details and exit

-v {debug,info,warning,error,critical},
--verbose {debug,info,warning,error,critical}
    Logging verbosity level    
```

## Example Commands

### Help
```bash
pyfwimagebuilder --help
```

### Example Usage:

Building an image:
```bash
pyfwimagebuilder build -i myapp.hex -c myconfig.toml -o myimage.img
```

Decoding an image:
```bash
pyfwimagebuilder decode -i myapp.img -c myconfig.toml -o myimage.txt
```