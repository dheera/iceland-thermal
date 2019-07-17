# High-Res Thermal Photos of Iceland

Original thermal data for all of the images. Documentation will be completed shortly.

* colormap.json -- a color scale for each image
* thermal.zip -- original radiometric data from the thermal camera
* thermal.tiff -- panoramic stitched thermal data
* visible.tiff -- corresponding monochrome visible light image from a regular SLR
* scripts/apply-colormap.py -- creates pretty images from the above
* scripts/seek2gray -- converts a radiometric TIFF (raw output from Seek RevealPro) to an 8-bit TIFF using a givin min/max temperature to correspond to 0 and 255

Example:
```
scripts/apply-colormap.py cave
```

More documentation coming soon


