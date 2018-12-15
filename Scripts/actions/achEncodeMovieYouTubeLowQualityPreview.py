"""Encode Movie YouTube Low Quality Preview Script - V1.0 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will send the currently selected media to Compressor and encode a MP4 file. 

The words "YouTube Low Quality Preview" literally means it encodes an MP4 that is soo bad, so low fi, so compressed, and very terrible looking you can't use it for content delivery. 

This is actually intentional so you have a visual quick to run script that can be used locally as a video encoding diagnostics tool.

The badly compressed output lets you see visually and know what aspects of your comp such as large amounts of randomized grain, or high motion areas, are sucking up your very precious and very limited video bandwidth.

A "YouTube Quality Preview" movie output created using this script should *never ever* be used to deliver footage or content to *anyone*. It looks, and is really terrible quality output. That's intentional. This is a preview tool to previz your movie going up to YouTube, and then being viewed on a typical consumer's system with run of the mill hardware and network bandwidth,

The reason this script exists at all is to let you, the comp artist, the content creator, check for and anticipate the horrors of MP4 video blocking, glitches, banding, temporal stuttering, or other codec issue you would not normally see immediatly. This puts you in control of QA processes for video encoding. To allow *YOU*, the original artist to decide on the appropriate tweaks and changes that might need to happen vs allowing someone else to dictate that to you days later after you hand them simply beautiful looking 16-bit half-float EXR image sequences that look fine and are fine.

It is video encoding for the web that potentially breaks the creative intent you want. And now you can know what that process will do to your art while still inside of SilhouetteFX . :) 

Without this "Encode Movie > YouTube LQ" tool you would typically have to wait until long after you've exported and encoded your high quality video master, uploaded it to YouTube, waited in a queue for the video to process, and finally get a notification email that your video is ready.

Then you watch the video and will be completely shocked and horrified at the results of what low bit rate compressed quality video does on the web in 2018.

Well, horrified, compared to the beautiful media you started with, the footage you saw the moment before you did the SilhouetteFX based "Session > Render Session" menu item task, then the "Actions > Encode Movie >" menu item video encoding thing, and uploaded your movie to YouTube. :LOL:

# Script Usage # 

Step 1. Select a source media node in the tree.

Step 2. Run the "Actions > Encode Movie" menu item.

# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/EncodeMovieYouTubeLowQualityPreview.py

Step 3. Copy the provided Apple Compressor encoding presets folder named "compressor" to:

/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/compressor

The compressor folder is used as a container to neat and tidily hold your exported ".cmprstng" file.

Step 4. Scroll down in this document and update that filepath and the name of the Apple Compressor exported ".cmprstng" preset file you want to use with the current "achEncodeMovie.py" script.

	# Compressor preset
	settings = '/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/compressor/YouTubeLowQualityPrevie.cmprstng'

Step 5. Restart SilhouetteFX to re-load the active scripts, and start creating new art, new possibilities, and making new creative visions come to life!

# Bonus Tip #

Apple Compressor's CLI mode expects your image sequence to be rendered into a new, custom output folder. The files present in that folder, in linear order will be turned into your movie file.

Compressor can work with DWAA encoded EXRs that have RGBA data in them. You will have to use SilhouetteFX and its Render Session mode to bounce out a temporary RGBA channel EXR sequence if you want to encode an MP4 or ProRes movie from it using this script.
.
"""

# Import the modules
from fx import *
from tools.objectIterator import ObjectIterator
import hook

# Return the Source node's master source clip
def GetSource(node):
	if node:
		if node.type == 'SourceNode':
			props = node.properties
			primary = props['stream.primary']
			return primary.getValue()
		
		input = node.getInput()
		if input.pipes:
			return GetSource(input.pipes[0].source.node)
	return None

# Return the Output node's filepath
def GetOutput(node):
	import fx
	
	# Get the session
	session = fx.activeSession()
	
	if node:
		if node.type == 'OutputNode':
			# Build the current frame
			padding = int(fx.prefs['render.filename.padding'])
			startFrame = session.startFrame
			currentFrame = int(startFrame + fx.player.frame)

			# Build the file format
			formatList = ('.cin', '.dpx', '.iff', '.jpg', '.exr', '.png', '.sgi', '.tif', '.tga')
			format = node.properties['format'].value
			formatFancy = formatList[format]
	
			# Build the filename
			path = node.properties['path'].value + '.' + str(currentFrame).zfill(padding) + formatFancy
			return path
			
	return None

# Compress a movie from the folder path
def EncodeMovie(path):
	import os
	import subprocess
	
	# Trim the filepath down to the parent folder
	dir = os.path.dirname(path)
	
	# Compressor preset
	settings = '/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/compressor/YouTubeLowQualityPreview.cmprstng'
	
	# Compressor Job name
	batch = 'sfx+'
	
	# Movie Extension
	ext = 'mp4'
	
	# Make the output movie filename
	dest = dir + os.sep + 'YouTube_1MBIT_Encode.' + ext
	
	# Build the Compressor launching command
	cmd = '/Applications/Compressor.app/Contents/MacOS/Compressor'
	args = [cmd, '-batchname', batch, '-jobpath', dir, '-settingpath', settings, '-locationpath', dest]
	print('\t[Launching Compressor] ' + str(args))
	
	# Run Compressor
	# subprocess.call(args)
	subprocess.Popen(args)

# Run the script
def run():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[Encode Movie YouTube Low Quality Preview]')
	print('\t[Node Name] ' + node.label)
	
	# Start the undo operation
	fx.beginUndo('Encode Movie')
	
	# Process a source node
	if node.type == 'SourceNode':
		# Find the active source node
		source = GetSource(node)
		if source:
			# Get the current node's filepath
			path = source.path(-1)
			print('\t[Image] ' + path)
			
			# Generate the movie
			EncodeMovie(path)
		else:
			print('\t[Error] Select a Source or Output Node.')
	elif node.type == 'OutputNode':
		# Find the active OutputNode path
		path = GetOutput(node)
		print('\t[Image] ' + path)
		
		# Generate the movie
		EncodeMovie(path)
	else:
		print('\t[Error] Select a Source or Output Node.')
	
	# Finish the Undo operation
	fx.endUndo()

# Create the action
class EncodeMovieYouTube(Action):
	"""Encode a movie in Compressor."""
	
	def __init__(self):
		Action.__init__(self, 'Encode Movie|YouTube LQ')
		
	def available(self):
		assert len(selection()) != 0, 'Select a Source or Output node.'
		
	def execute(self):
		run()

addAction(EncodeMovieYouTube())

