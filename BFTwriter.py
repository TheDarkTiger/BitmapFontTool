#!/usr/bin/env python3
#
# Bitmap Font Tools : Writer
# I was just tired to copy/paste bitmap fonts...
# Greetings KAB, Dul, and Stefan Pettersson ;) (see ReadMe for more info)
# 
# 2022 [TheDarkTiger]

import os
import argparse
import PIL
from PIL import Image, ImageDraw


#def main() :

# Parse arguments
parser = argparse.ArgumentParser( description = "Bitmap Font Tool : Writer. Writes text using a bitmap font." )
parser.add_argument( "-b", "--bitmap", help = "Font's bitmap ('font.png' if none specified)" )
parser.add_argument( "-t", "--text", help = "Text to render ('Test!' if none specified)" )

args = parser.parse_args()
if args.bitmap:
	fontImageFile = args.bitmap
else :
	fontImageFile = "font.png"

if args.text:
	lines = [args.text]
else :
	lines = ["Test!"]

silent = False

# Normalize paths
fontImageFile = os.path.realpath( fontImageFile )
fontName = os.path.basename( fontImageFile ).split( "." )[0]
fontPath = os.path.dirname( fontImageFile )

# Font caracteristics
font = {}
font["image"] = Image.open( fontImageFile ).convert('RGBA')
font["notes"] = "Nada poney."
font["height"] = 8
font["width"] = 16
font["char"] = {}
font["char"]["mode"] = "packed"
font["char"]["start"] = 0
font["char"]["end"] = 127
font["char"]["height"] = 8
font["char"]["width"] = 8
font["char"]["space"] = 0


# Print infos
if not silent :
	print( f"Processing {lines[0]} using {fontImageFile}..." )
	if "notes" in font :
		print( "Font notes: ",font["notes"] )
	


# Text generation
char_width = 0
for line in lines :
	if len( line ) > char_width :
		char_width = len( line )
char_height = len( lines )

width = char_width*font["char"]["width"]
height = char_height*font["char"]["height"]

renderedText = Image.new( "RGBA", ( width, height ), (255,0,255,0) )


# Draw text
x = 0
y = 0
for line in lines :
	x = 0
	for char in line :
		
		# Get the char index
		charIndex = ord( char )
		
		# If the char is on the font
		if (charIndex >= font["char"]["start"]) and (font["char"]["end"]) :
			charIndex -= font["char"]["start"]
			# Compute the coords in font of the char
			if font["char"]["mode"] == "packed" :
				u = ( charIndex%font["width"] * font["char"]["width"])
				v = ( int( charIndex/font["width"] ) * font["char"]["height"])
			else :
				u, v = (0,0)
		
		# Blit the char into the destination image
		renderedText.paste( font["image"].crop((u,v, u+font["char"]["width"],v+font["char"]["height"])), (x,y) )
		#renderedText.putpixel( (x,y), c_purple )
		
		x += font["char"]["width"]
	y += font["char"]["height"]


# Save the rendered text
renderedTextPath = os.path.join( fontPath, f"{fontName} - text.png" )
renderedText.save( renderedTextPath, "png" )
