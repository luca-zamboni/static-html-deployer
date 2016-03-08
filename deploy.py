
import os
from os import listdir
from os.path import isfile, join
import re
import distutils.dir_util
from subprocess import call
import shutil as sh
import tempfile


compiled = "deploy/"
mypath = "include/"

all_html = [ f for f in listdir("./") if isfile(join("./",f)) ]
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

def remove_less(content):
	content = re.sub('stylesheet/less',"stylesheet",content)
	content = re.sub(r'\.less','.css',content)

	content = re.sub(r'.*less\.min\.js.*','',content)
	content = re.sub(r'.*less\.js.*','',content)
	return content

def link_css_min(content):

	css_reg = re.findall(r'css/.*[^m][^i][^n]\.css',content)
	for css in css_reg:
		content = re.sub(css,css[0:-4]+".min.css",content)


	return content


def link_js_min(content):

	js_reg = re.findall(r'js/.*[^m][^i][^n]\.js', content)
	for js in js_reg:
		content = re.sub(js, js[0:-3] + ".min.js", content)

	return content


def compile_and_min():
	for filecss in os.listdir(compiled + "css/"):
		if filecss.endswith(".less"):
			os.system("lessc " + compiled + "css/" + filecss + " > " +
					compiled + "css/" + re.sub(".less", "", filecss) + ".css")
			os.remove(compiled + "css/" + filecss)

	for filecss in os.listdir(compiled + "css/"):
		if(not "min" in filecss and "css" == filecss[-3:]):
			os.system("yui-compressor " + compiled + "css/" + filecss +
					 " > " + compiled + "css/" + re.sub(".css", ".min.css", filecss))
			os.remove(compiled + "css/" + filecss)
			pass

	for filejs in os.listdir(compiled + "js/"):
		if(not ".min." in filejs and "js" == filejs[-2:]):
			os.system("yui-compressor " + compiled + "js/" + filejs +
						" > " + compiled + "js/" + re.sub(".js", ".min.js", filejs))
			os.remove(compiled + "js/" + filejs)
			pass


def copy_dir():
	copy = ["img/","fonts/","data/"]
	for cp_dir in copy:
		distutils.dir_util.copy_tree(cp_dir,compiled + cp_dir)
	copy_min = ["css/","js/"]
	for cp_dir in copy_min:
		if not os.path.exists(compiled + cp_dir):
			os.makedirs(compiled + cp_dir)
		for f in os.listdir(cp_dir):
			if "min" in f:
				open(compiled + cp_dir + f,'w')
				sh.copy(cp_dir + f, compiled + cp_dir + f)
		#distutils.dir_util.copy_tree(cp_dir,compiled + cp_dir)


def get_css_files(content):

	all_css = re.findall(r'<link .* href="(.*)" />', content)

	return all_css

def include_css(content):

	css_buffer = ""

	all_css = get_css_files(content)
	for css in all_css:
		with open(compiled+css,'r') as f:
			css_text = f.read()
			css_buffer += css_text

	content = re.sub('</head>',"<style>"+css_buffer+"</style></head>",content)

	return content

def elaborate_html(content):
	all_include = re.findall(r'<div class="include">.*</div>', content)
	all_include = [re.sub('<div class="include">','',a) for a in all_include]
	all_include = [re.sub('</div>','',a) for a in all_include]
	for inc in all_include:
		for f in files:
			if inc + ".html" == f:
				#print(inc)
				with open(mypath+ f, 'r') as content_file:
					content_to_include = content_file.read()
					content = re.sub(r'<div class="include">'+inc+'</div>',content_to_include,content)
	#print(content)

	content = remove_less(content)

	content = link_css_min(content)
	content = link_js_min(content)

	# Abviusly not vorking
	#content = include_css(content)

	return content

def compile_html():
	for file_html in os.listdir("./"):
		if file_html.endswith(".html"):
			with open(file_html, 'r') as content_file:
				content = elaborate_html(content_file.read())

				out_file = open(compiled + file_html,"w")
				out_file.write(content)
				out_file.close()

def main():

	copy_dir()

	# compile_and_min()

	compile_html()


main()
