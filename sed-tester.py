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
	editor = ["vim"] # editor with optional cli args e.g. 
	                   # ["vim","-S"] or ["vim"] or ["gedit"] or ["nano"] etc.
	                   #use cli editors as gui editors loose focus
	
	
	def upss():
		# update sed script
		cmd = editor.copy() # make a copy so the original editor var doesnt get updated
		cmd.extend([sedscriptfile])
		subprocess.run(cmd)
		
	def upinp():
		# update  inp file data
		cmd = editor.copy() # make a copy so the original editor var doesnt get updated
		cmd.extend([inpfile])
		subprocess.run(cmd)
	
	def upssandinp():
		#update sed script and input file together
		vim_hopen_opt = "-o"
		vim_vopen_opt = "-O"
		vim_extra_opts = ["-c",":set numbers", "-c", ":bo term"]
		act_vim_open_opt = vim_vopen_opt
		if "vim" in editor:
			cmd = editor.copy()
			cmd.extend(vim_extra_opts)
			cmd.extend([act_vim_open_opt, sedscriptfile, act_vim_open_opt, inpfile])
			subprocess.run(cmd)
		else:
			print("Sorry, this option only available for vim as editor.")
			print("Try using options 2 or 3.")
		
	def prss(wait=False):
		# print sed script
		subprocess.run(["cat", sedscriptfile])
		if (wait == True):
			input("EOF. Press a key to continue...")
	
	def prinp(wait=False):
		# print sed script
		subprocess.run(["cat", inpfile])
		if (wait == True):
			input("EOF. Press a key to continue...")
		
	def prssninp():
		# print sed script and input
		print("\n===> SED SCRIPT:")
		prss(wait = False)
		print("===> INPUT DATA:")
		prinp(wait = False)
		print("===> END.")
	
	def runss():
		# print sed script and input
		prssninp()
		#run sed script
		print("\n===> SED OUTPUT:")
		subprocess.run(["sed", "-f", sedscriptfile, inpfile])
		print("===> END SED OUTPUT.\n\n")
		
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

	def runssdebug():
		pass
		
	while (True):
		print("")
		q = "What do you want to do?:"
		q += "\n1. Print sed script & input data"
		q += "\n2. update sed script"
		q += "\n3. Update input data"
		q += "\n4. Update script and input data"
		q += "\n5. Run sed"
		q += "\n6. Run sed -n"
		q += "\n7. Run sed -l"
		q += "\n8. Run sed --debug"
		q += "\nx. Type \'x\' or \'q\' to quit"
		valid_start_opt_int = 1
		valid_end_opt_int = 8
		print(q)
		try:
			c = input("Enter choice: ")
			if c in ["x","q"]:
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
			if c<valid_start_opt_int or c>valid_end_opt_int:
				raise InvalidChoiceError("")
		except (ValueError, InvalidChoiceError):
			print("\nInvalid choice. ",end='')
			continue
		
		if c == 1:
			prssninp()
			input() # just dont display the menu immediately
		if c == 2:
			upss()		
		if c == 3:
			upinp()
		if c == 4:
			upssandinp()
		if c == 5:
			runss()
			input() # just dont display the menu immediately
		if c == 6:
			sedargs = "-n" #input("Enter seprated list of args for sed\n (except -f) e.g. \'-n\':")
			runssc(sedargs)
			input() # just dont display the menu immediately
		if c == 7:
			sedargs = "-e l" #input("Enter seprated list of args for sed\n (except -f) e.g. \'-n\':")
			runssc(sedargs)
			input() # just dont display the menu immediately
		if c == 8:
			sedargs = "--debug" #input("Enter seprated list of args for sed\n (except -f) e.g. \'-n\':")
			runssc(sedargs)
			input() # just dont display the menu immediately
			

# call main function
main()
		
	
		
		
