#!/usr/bin/env python3

import numpy
import cv2
import sys
import json
import os

IMAGE = sys.argv[1]

fn_c = IMAGE + '/stitchalign/colormap.json'
fn_t = IMAGE + '/stitchalign/thermal.tiff'
fn_v = IMAGE + '/stitchalign/visible.tiff'
fn_mapped = IMAGE + '/mapped.tiff'
fn_scale = IMAGE + '/scale.tiff'
fn_layout = IMAGE + '/layout.svg'
fn_out = IMAGE + '/out.png' 

print("Reading color map ...")
with open(fn_c, 'r') as f:
    colormap_keypoints = json.loads(f.read())

tmin = colormap_keypoints[0][0]
tmax = colormap_keypoints[-1][0]
print("tmin = ", tmin, " tmax = ", tmax)

colormap = numpy.array([ [0, 0, 0] ] * 256, dtype = numpy.uint8)
alphamap = numpy.array([ 0.0 ] * 256, dtype = numpy.float)

j = 0
tminj = tmin
tmaxj = colormap_keypoints[j+1][0]
for i in range(256):
    ti = (i/256)*(tmax - tmin) + tmin
    if ti > tmaxj:
        j += 1
        tminj = tmaxj
        tmaxj = colormap_keypoints[j+1][0]
    frac = (ti - tminj) / (tmaxj - tminj)
    colormap[i, :] = frac*numpy.array(colormap_keypoints[j+1][1]) + (1-frac)*numpy.array(colormap_keypoints[j][1])
    alphamap[i] = frac*numpy.array(colormap_keypoints[j+1][2]) + (1-frac)*numpy.array(colormap_keypoints[j][2])

img_t = cv2.imread(fn_t)[:,:,1]
print("Read thermal image, shape = ", img_t.shape)

img_tc = colormap[img_t].astype(numpy.uint8)
img_ta = alphamap[img_t]
print("Mapped thermal image, shape = ", img_tc.shape)
img_tc_hsv = cv2.cvtColor(img_tc, cv2.COLOR_BGR2HSV)

img_v = cv2.imread(fn_v)
print("Read visual image, shape = ", img_v.shape)
img_v_hsv = cv2.cvtColor(img_v, cv2.COLOR_BGR2HSV)

img_mapped = numpy.copy(img_v_hsv)
img_mapped[:,:,0] = img_tc_hsv[:,:,0]
img_mapped[:,:,1] = img_tc_hsv[:,:,1]
img_mapped[:,:,2] = img_v_hsv[:,:,2] * (1 - img_ta) + img_tc_hsv[:,:,2] * img_ta

img_mapped = cv2.cvtColor(img_mapped, cv2.COLOR_HSV2BGR)
cv2.imwrite(fn_mapped, cv2.resize(img_mapped, (4096, 2731)))

scale = numpy.repeat(numpy.arange(0,256,1),32).reshape((256,32)).T
img_scale = colormap[scale]
cv2.imwrite(fn_scale, img_scale)

template = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   version="1.1"
   id="svg2"
   width="4096"
   height="2731"
   viewBox="0 0 4096 2731"
   sodipodi:docname="template2.svg"
   inkscape:version="0.92.3 (2405546, 2018-03-11)">
  <metadata
     id="metadata8">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs6" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="1366"
     inkscape:window-height="812"
     id="namedview4"
     showgrid="false"
     inkscape:zoom="0.14208984"
     inkscape:cx="1820.7852"
     inkscape:cy="1775.4366"
     inkscape:window-x="0"
     inkscape:window-y="32"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg2" />
  <image
     xlink:href="{{img_mapped}}"
     y="0"
     x="0"
     id="image10"
     preserveAspectRatio="none"
     height="2731"
     width="4096" />
  <image
     xlink:href="{{img_scale}}"
     width="768"
     height="32"
     preserveAspectRatio="none"
     id="image652"
     x="3146"
     y="177.56262" />
  <text
     xml:space="preserve"
     style="font-style:normal;font-weight:normal;font-size:50px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:0.8;stroke:none"
     x="3146.0000"
     y="266.60001"
     id="text657"><tspan
       sodipodi:role="line"
       id="tspan655"
       x="3146.0000"
       y="266.60001"
       style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-family:Mentone;-inkscape-font-specification:Mentone;fill:#ffffff">{{tmin}} C</tspan></text>
  <text
     xml:space="preserve"
     style="font-style:normal;font-weight:normal;font-size:50px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:0.8;stroke:none"
     x="3916"
     y="266.60001"
     id="text657-3"><tspan
       sodipodi:role="line"
       id="tspan655-6"
       x="3916"
       y="266.60001"
       style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-family:Mentone;-inkscape-font-specification:Mentone;text-align:end;text-anchor:end;fill:#ffffff">{{tmax}} C</tspan></text>
</svg>
"""

template = template.replace('{{tmin}}', str(int(tmin))).replace('{{tmax}}', str(int(tmax))).replace('{{img_mapped}}', fn_mapped).replace('{{img_scale}}', fn_scale)

with open(fn_layout, 'w') as f:
    f.write(template)

os.system('inkscape -e %s %s' % (fn_out, fn_layout))
