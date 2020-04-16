# ARTS tools
[![Build Status](https://travis-ci.com/loostrum/arts_tools.svg?branch=master)](https://travis-ci.com/loostrum/arts_tools)  
Processing scripts for Apertif Radio Transient System data

## Requirements
* Python >= 3.6
* Numpy >= 1.17
* Astropy

## Installation
`pip install arts_tools`

## Fixing archival FITS files
FITS files retrieved from the Apertif Long-Term Archive (ALTA) from before 2020/04/08 can be made readable with 
`arts_fix_fits_from_before_20200408 file.fits`. These fixes are applied:
1. The NAXIS2 value in the header is changed from zero to the correct value
2. The data size is expressed in bytes instead of bits
3. The frequency and time axes of the data are swapped
4. The frequency order of the data and weights, scales, offsets, and frequencies columns is flipped

By default, the script appends `_fixed` to the filename. Run `arts_fix_fits_from_before_20200408 -h` for more options.

#### Note for Science Verification Campaign data
Data from the SVC has a correct NAXIS2 value in some cases. However, the other fixes do need to be applied. 
This can be forced by running `arts_fix_fits_from_before_20200408 --force file.fits`.

## Reading parametersets
The FITS headers contain an encoded observation parameterset. To print the parameterset, use 
`arts_read_parameterset file.fits`. It can also be loaded in python as a dictionary with:
```python
from arts_tools.fits.reader import read_parameterset
parset = read_parameterset('/path/to/file.fits')
```
Note that all values are read as strings.