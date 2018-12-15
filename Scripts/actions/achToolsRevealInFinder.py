"""
Reveal in Finder Script - V1.0 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will reveal the currently selected media in a Finder folder view.

# Script Usage # 

Step 1. Select a Source or Output node in the tree.

Step 2. Run the "Actions > Tools > Reveal in Finder" menu item.

# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/ToolsRevealInFinder.py

Step 3. Restart SilhouetteFX to re-load the active scripts.
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
			return getSource(input.pipes[0].source.node)
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

# Run a shell command
def Command(path):
	import os
	import subprocess
	
	# Trim the filepath down to the parent folder
	dir = os.path.dirname(path)
	
	# Make the output movie filename
	dest = dir + os.sep
	
	# Build the launching command
	cmd = 'open'
	args = [cmd, dest]
	print('\t[Launching Open] ' + str(args))
	
	# Run Open
	# subprocess.call(args)
	subprocess.Popen(args)

# Run the script
def run():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[Reveal in Finder]')
	print('\t[Node Name] ' + node.label)
	
	# Process a source node
	if node.type == 'SourceNode':
		# Find the active source node
		source = GetSource(node)
		if source:
			# Get the current node's filepath
			path = source.path(-1)
			print('\t[Image] ' + path)
			
			# Reveal in Finder
			Command(path)
		else:
			print('\t[Error] Select a Source or Output Node.')
	elif node.type == 'OutputNode':
		# Find the active OutputNode path
		path = GetOutput(node)
		print('\t[Image] ' + path)
		
		# Reveal in Finder
		Command(path)
	else:
		print('\t[Error] Select a Source or Output Node.')


# Create the action
class RevealInFinder(Action):
	"""Encode a movie in Compressor."""
	
	def __init__(self):
		Action.__init__(self, 'Tools|Reveal in Finder')
		
	def available(self):
		assert len(selection()) != 0, 'Select a media object.'
		
	def execute(self):
		run()

addAction(RevealInFinder())
