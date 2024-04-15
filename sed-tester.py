#!/bin/python3

import subprocess
import sys
import os
import subprocess


class InvalidChoiceError(Exception):
	pass

class NormalExitException(Exception):
	pass


def main():
	scriptdir = os.path.dirname(os.path.realpath(__file__))
	sed_script = ""
	input_data = ""
	datadir = os.path.join(scriptdir,"tools_data")
	if not os.path.exists(datadir):
		os.makedirs(datadir)
	sedscriptfile = os.path.join(datadir,"sed-script.sed")
	inpfile = os.path.join(datadir,"sed-input.txt")
	editor = ["vim"] # editior with optional cli args e.g. 
	                   # ["vim","-S"] or ["vim"] or ["gedit"] or ["nano"] etc.
	                   #use cli editors as gui editors loose focus
	
	
	def upss():
		# update sed script
		cmd = editor.copy() # make a copy so the original editor var doesnt get updated
		cmd.extend([sedscriptfile])
		subprocess.run(cmd)
		
	def upinp():
		# update  inp file data
		cmd = editor.copy # make a copy so the original editor var doesnt get updated
		cmd.extend([inpfile])
		subprocess.run(cmd)
		
	def prss(wait=False):
		# print sed script
		subprocess.run(["cat", sedscriptfile])
		if (wait==True):
			input("EOF. Press a key to continue...")
	
	def prinp(wait=False):
		# print sed script
		subprocess.run(["cat", inpfile])
		if (wait==True):
			input("EOF. Press a key to continue...")
		
	def prssninp():
		# print sed script and input
		print("\n===> SED SCRIPT:")
		prss(wait=False)
		print("===> INPUT DATA:")
		prinp(wait=False)
		print("===> END.")
		input()
	
	def runss():
		# print sed script and input
		prssninp()
		#run sed script
		print("\n===> SED OUTPUT:")
		subprocess.run(["sed", "-f", sedscriptfile, inpfile])
		print("===> END SED OUTPUT.\n\n")
		input() # just dont display the menu immediately
		
	def runssc(cargs):
		# cargs must be a string e.g. "" or "-n" or "-arg1,-arg2" 
		# print sed script and input
		#run sed script with cargs(custom comma separated args)
		h = ["sed"]
		m = cargs.split(",")
		t = ["-f", sedscriptfile, inpfile]
		cmd = []
		cmd = h
		cmd.extend(m)
		cmd.extend(t)
		print(f"running sed wih args {m}\n")
		prssninp()
		print("\n===> SED OUTPUT:")
		subprocess.run(cmd)
		print("===> END SED OUTPUT.\n\n---")
		input()

		
	while (True):
		print("")
		q = "What do you want to do?:"
		q += "\n1. Print sed script & input data"
		q += "\n2. update sed script"
		q += "\n3. Update input data"
		q += "\n4. Run sed"
		q += "\n5. Run sed, custom flags (except -f)"
		q += "\nx. Type \'x\' to quit"
		print(q)
		try:
			c = input("Enter choice: ")
			if c == "x":
				raise NormalExitException("")
		except (EOFError,KeyboardInterrupt, NormalExitException) as e:
			if type(e) == EOFError:
				print("\nReceived EOF")
			elif type(e) == KeyboardInterrupt:
				print("\nReceived KeyboardInterrupt")
			elif type(e) == NormalExitException:
				pass # just terminate flow gracefully
			print("Exiting...\n")
			exit()

		try:
			c = int(c)
			if c<1 or c>5:
				raise InvalidChoiceError("")
		except (ValueError, InvalidChoiceError):
			print("\nInvalid choice. ",end='')
			continue
		
		if c==1:
			prssninp()
		if c==2:
			upss()
		if c==3:
			upinp()
		if c ==4:
			runss()
		if c==5:
			sedargs = input("Enter seprated list of args for sed\n (except -f) e.g. \'-n\':")
			runssc(sedargs)
			

# call main function
main()
		
	
		
		
