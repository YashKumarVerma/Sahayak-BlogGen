""" 
Created By : Yash Kumar verma
https://github.com/YashKumarVerma/Sahayak-BlogGen
"""
from pathlib import Path
import sys
from subprocess import call
import os
import time
from time import gmtime, strftime
from distutils.dir_util import copy_tree
import pip
import shutil

# get configuration file
config = Path("config.ykv");

#new line function
def line():
	# Just a fancy new line
	# print("\n - - - - - - - - - - - - - - - - - - \n");
	print("\n ========================================================== \n");

def singleLine():
	print("\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n");
	

def newPage():
	os.system("cls");
	line();
	print("\n\n    THE STATIC SITE GENERATOR  \n");
	line();

# install
def install():
	newPage()
	print ("\n\n Starting Installation Process ... \n")

	# creating file
	config = open("config.ykv","w",encoding="utf8");

	# Get Name
	print("\n\n -----------------------------------\n\n ")
	title 		= input("\n Enter Title of site : ")
	subTitle	= input("\n Enter Sub title of site : ")
	baseURL 	= input("\n Enter Base URL of Site : ")
	authorName  = input("\n Enter Name of Author : ")
	footerText 	= input("\n Enter Text For Footer : ")
	authorEmail = input("\n Enter author email : ")
	
	print("\n Place the author's photo in assets/images as author.jpg once site renders. ");
	print("\n\n -----------------------------------\n\n ")
	print("All configurations done. Installing markdown compiler ... ");

	pkgs = ['markdown2']
	for package in pkgs:
	    try:
	        import package
	    except ImportError:
		    pip.main(['install', package])

	config.write(title 			+"\n")
	config.write(subTitle 		+"\n")
	config.write(baseURL 		+"\n")
	config.write(authorName 	+"\n")
	config.write(authorEmail	+"\n")
	config.write("assets/images/author.jpg")

# THE POST FUNCTIONS
def listPost():
	newPage();
	print(" Listing all posts ... ");
	line();

	#get data
	data = open("warehouse/post.ykv","r",encoding="utf8");
	data = data.readlines();
	singleLine();
	for x in data:
		x = x.strip();
		x = x.split("~~!~~");
		print("UID : " + x[0] );
		print("\t Title : " + x[1]);
		print("\t Date  : " + x[2]);
		print("\t Slug  : " + x[3]);
		print("\t Desc	: " + x[4]);
		singleLine();
	input("\n Press any key to go back to menu : ");
	menu();

def createPost():
	newPage();
	print(" Creating new post ...  ");
	line();

	file 	= open("warehouse/uid.ykv","r",encoding="utf8");
	data 	= file.read().strip();
	uniId   = str(int(data)+1);
	file.close();

	file 	= open("warehouse/uid.ykv","w",encoding="utf8");
	file.write(uniId);
	file.close();

	# post count
	file 		= open("warehouse/postCount.ykv","r",encoding="utf8");
	postCount	= file.read().strip();
	file.close();
	file 		= open("warehouse/postCount.ykv","w",encoding="utf8");
	postCount	= str(int(postCount)+1);
	file.write(postCount);
	file.close();

	# Create New Post
	postUID  = uniId;
	postName = input("Enter Title for Post : ");
	postTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());
	postSlug = input("Enter url slug for Post : ");
	postDesc = input("Enter short summary of post for listing :  ");
	data 	 = postUID+"~~!~~"+postName+"~~!~~"+postTime+"~~!~~"+postSlug+"~~!~~"+postDesc+"\n";
	
	# append to posts
	file = open("warehouse/post.ykv","a+",encoding="utf8");
	file.write(data);
	file.close();
	
	# create file for post
	x = open("warehouse/posts/"+postUID+".ykv.md", "w+",encoding="utf8");
	y = open("warehouse/posts/default.ykv","r",encoding="utf8");
	ydata = y.read();
	x.write(ydata);
	x.close();
	y.close();

	line();
	print("\n Post Created. Please Enter the content in Markdown. Opening File... Please wait. \n ")
	print(" You can close this window, write the post, and then return to the program. \n\n\n Cheers !");
	line();

	os.system("cd warehouse/posts/ & "+postUID+".ykv.md");
	menu();

def deletePost():
	newPage();
	print(" Deleting Posts ...  ");
	line();

	file = open("warehouse/post.ykv","r+",encoding="utf8");
	data = file.readlines();
	file.close();

	singleLine();
	for x in data:
		x = x.strip();
		x = x.split("~~!~~");
		print("UID : " + x[0] );
		print("\t Title : " + x[1]);
		print("\t Date  : " + x[2]);
		print("\t Slug  : " + x[3]);
		print("\t Desc  : " + x[4]);
		singleLine();

	uid = input("Enter uid of post to delete. This action cannot be reverted ! : ");
	opt = input("Enter uid again to delete post : ");

	if(uid == opt):
		# Delete the file
		os.remove("warehouse/posts/"+uid+".ykv.md");
		
		newPostFile = "";
		for x in data:
			x = x.strip();
			x = x.split("~~!~~");
			# for y in 
			if(x[0] != uid):
				newPostFile += x[0]+"~~!~~"+x[1]+"~~!~~"+x[2]+"~~!~~"+x[3]+"~~!~~"+x[4]+"\n"; 
		
		os.remove("warehouse/post.ykv");
		file = open("warehouse/post.ykv","w+",encoding="utf8");
		file.write(newPostFile);
		file.close();
		
		file = open("warehouse/postCount.ykv",'r+',encoding="utf8");
		data = file.read();
		file.close();
		
		file = open("warehouse/postCount.ykv",'w',encoding="utf8");
		file.write(str(int(data)-1));
		file.close();

		print("\n Post Deleted");
		time.sleep(2);
		menu();

def editPost():
	newPage();
	print(" Editing Posts ...  ");
	line();
	
	file = open("warehouse/post.ykv","r+",encoding="utf8");
	data = file.readlines();
	file.close();

	singleLine();
	for x in data:
		x = x.strip();
		x = x.split("~~!~~");
		print("UID : " + x[0] );
		print("\t Title : " + x[1]);
		print("\t Date  : " + x[2]);
		print("\t Slug  : " + x[3]);
		print("\t Desc  : " + x[4]);
		singleLine();

	uid = input("Enter uid of post to Edit : ");
	opt = input("Enter uid again to edit post : ");

	postFile = Path("warehouse/posts/"+uid+".ykv.md");
	if(not postFile.is_file()):
		print("\n Invald UID ! ");
		time.sleep(2);
		menu();

	if(uid == opt):
		eTitle 		= input("\n\n\t Enter new title : ");
		eTime  		= input("\n\t Enter new Date : ");
		eSlug  		= input("\n\t Enter new Slug : ");
		eDesc 		= input("\n\t Enter new summary :");
		editdata 	= uid+"~~!~~"+eTitle+"~~!~~"+eTime+"~~!~~"+eSlug+"~~!~~"+eDesc+"\n";
		
		# open post for user
		os.system("cd warehouse/posts/ & "+uid+".ykv.md");

		# create the file again
		file = open("warehouse/post.ykv","r+",encoding="utf8");
		data = file.readlines();
		file.close();
		contentForFile = "";
		for x in data:
			x = x.strip().split("~~!~~");
			# print("\n\n\n\n");
			# print(x);
			# print("\n\n\n\n");
			if(x[0]==uid):
				contentForFile 	+= editdata; 
			else:
				contentForFile 	+= x[0]+"~~!~~"+x[1]+"~~!~~"+x[2]+"~~!~~"+x[3]+"~~!~~"+x[4]+"\n";

		#write now
		file =open("warehouse/post.ykv","w",encoding="utf8");
		file.write(contentForFile);
		file.close();

		line();
		print("Post Edited !. Press any key to go back to menu.")
		input();
		menu();
	else:
		print("\n UID did not match !");
		time.sleep(2);
		menu();

def render():
	import markdown2

	if ( os.path.isdir("render")):
		print("\n\n\n RENDER FOLDER ALREADY EXIST. ");
		shutil.rmtree('render');
		print("\nRender folder empty now.")

	os.system("mkdir render")
	log = open("render/renderLog.ykv","w+",encoding="utf8");
	log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Render Started "+ "\n");
	
	themeName = input("\n Enter theme name :  ");
	if( not os.path.isdir("themes/"+themeName) ):
		print("\n Theme does not exist ! Loading default theme 'x' \n");
		log.write("Theme named " + themeName + " not found. Loading default theme 'x' " + "\n");
		themeName = 'x';

	print("\n Theme named " + themeName + " loaded. ");
	log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Theme Name : "+themeName + "\n");
	"""
		themeinfo
			0 - Theme Name 
			1 - Author Name
			2 - Author Email
	"""
	file = open("themes/"+themeName+"/themeInfo.ykv","r",encoding="utf8");
	themeinfo = file.readlines();
	file.close();
	
	"""
		config
			0-My Site
			1-Sub title
			2-http://www.mysite.com
			3-Yash
			4-yk.verma2000@gmail.com
			5-author image
	"""
	file = open("config.ykv","r",encoding="utf8");
	config = file.readlines();
	file.close();
	siteTitle 	= config[0].strip();
	siteSTitle 	= config[1].strip();
	url 		= config[2].strip();
	authorName  = config[3].strip();
	authorEmail = config[4].strip();
	authorImg   = config[5].strip();

	"""
		css
	"""
	file = open("themes/"+themeName+"/css.ykv",encoding="utf8");
	css = file.readlines();
	file.close();

	
	"""
		js
	"""
	file = open("themes/"+themeName+"/js.ykv",encoding="utf8");
	js = file.readlines();
	file.close();

	"""
		dir
	"""
	file = open("themes/"+themeName+"/dir.ykv",encoding="utf8");
	dirr = file.readlines();
	file.close();

	
	"""
		posts
	"""
	file = open("warehouse/post.ykv","r",encoding="utf8");
	posts = file.readlines();
	file.close();


	"""
		GET TEMPLATE 
	"""
	file = open("themes/"+themeName+"/structure/homepage.ykv.html","r",encoding="utf8");
	homepage = file.read();
	file.close();

	file = open("themes/"+themeName+"/structure/postListing.ykv.html","r",encoding="utf8");
	postListing = file.read();
	file.close();

	file = open("themes/"+themeName+"/structure/post.ykv.html","r",encoding="utf8");
	postDedicated = file.read();
	file.close();

	log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Data Extraction Successful  "+ "\n");

	"""
		Preparing Template 
	"""
	tempCSS = "";
	for x in css: 
		x = x.strip();
		tempCSS += "<link rel='stylesheet' type='text/css' href='" +url+ "assets/" +x+"'>\n";
	# open("tempcss.ykv","w").write(tempCSS);


	tempJS = "";
	for x in js:
		x = x.strip();
		tempJS += "<script type='text/javascript' src='" +url+"assets/" +x+ "'></script>\n";
	# open("tempjs.ykv","w").write(tempJS);

	"""
		Make The Posts
	"""
	os.system("cd render & mkdir posts");
	tempPost = "";
	for post in posts:
		tempStorage 		= postListing;
		tmpPostDedicated 	= postDedicated;
		post 		= post.strip().split("~~!~~");
		postUID  	= post[0]; 
		postTitle 	= post[1];
		postDate 	= post[2];
		postSlug 	= post[3];
		postDesc 	= post[4];
		file 		= open("warehouse/posts/"+postUID+".ykv.md",encoding="utf8");
		postContent = file.read();
		postContent = markdown2.markdown(postContent);
		file.close();
		os.system("cd render & cd posts & mkdir "+postSlug);
		log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Creating Post : "+postTitle + "\n");
		# postDesc

		tmpPostDedicated = tmpPostDedicated.replace("{{@css}}"				,tempCSS);
		tmpPostDedicated = tmpPostDedicated.replace("{{@js}}"				,tempJS);
		tmpPostDedicated = tmpPostDedicated.replace("{{@title}}"			,siteTitle);
		tmpPostDedicated = tmpPostDedicated.replace("{{@subTitle}}"			,siteSTitle);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postTitle}}" 		,postTitle);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postDate}}"			,postDate);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postDesc}}"	 		,postDesc);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postContent}}"	 	,postContent);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postSlug}}" 		,postSlug);
		tmpPostDedicated = tmpPostDedicated.replace("{{@url}}" 				,url);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postAuthor}}"		,authorName)
		tmpPostDedicated = tmpPostDedicated.replace("{{@authorImg}}"		,url+authorImg);
		tmpPostDedicated = tmpPostDedicated.replace("{{@postAuthorEmail}}" 	,authorEmail);

		file = open("render/posts/"+postSlug+"/index.html","w+",encoding="utf8");
		file.write(tmpPostDedicated);
		file.close();

		tempStorage = tempStorage.replace("{{@postTitle}}" 		,postTitle);
		tempStorage = tempStorage.replace("{{@postDate}}"		,postDate);
		tempStorage = tempStorage.replace("{{@postDesc}}"	 	,postDesc);
		tempStorage = tempStorage.replace("{{@postSlug}}" 		,postSlug);
		tempStorage = tempStorage.replace("{{@url}}" 			,url);
		tempStorage = tempStorage.replace("{{@authorImg}}"		,url+authorImg);
		tempStorage = tempStorage.replace("{{@postAuthorEmail}}",authorEmail);
		tempPost = tempPost +  tempStorage;

	"""
		Put data into template
	"""
	homepage = homepage.replace("{{@css}}"				,tempCSS);
	homepage = homepage.replace("{{@js}}"				,tempJS);
	homepage = homepage.replace("{{@title}}"			,siteTitle);
	homepage = homepage.replace("{{@subTitle}}"			,siteSTitle);
	homepage = homepage.replace("{{@posts}}" 			,tempPost);
	homepage = homepage.replace("{{@postAuthor}}"		,authorName);
	homepage = homepage.replace("{{@authorImg}}"		,url+authorImg);
	homepage = homepage.replace("{{@postAuthorEmail}}" 	,authorEmail);

	log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Homepage Generated  "+ "\n");
	

	# os.system("cd render & mkdir ")

	os.system("cd render & mkdir assets");
	
	for dirName in dirr : 
		dirName = dirName.strip();
		copy_tree("themes/"+themeName+"/"+dirName, "render/assets/"+dirName);
		log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Creating dir : " +dirName + "\n");
	
	open("render/index.html","w+",encoding="utf8").write(homepage);
	log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"|" +" Render Complete "+ "\n");
	print("\n Render Complete ");
	line();
	log.close();

	os.system("cd render & start .");
	input("\n Press any key to return to menu");
	menu();

def push():
	if ( os.path.isdir("git")):
		newPage();
		print("\n publishing to git repository ...");
		copy_tree("render", "git");

		# # log work around
		# file = open("render/renderLog.ykv","r");
		# log = file.read();
		# file.close();

		# file = open("git/renderLog.ykv","w+");
		# file.write(log);
		# file.close();

		commit = strftime("%Y-%m-%d %H:%M:%S", gmtime()) +" Automatic deploy"; 
		os.system('cd git & git add . & git commit -m "'+commit+'" & git push origin master ');

	else:
		newPage();
		print("\n git folder doesn't exist. Kindly create one and link it to repo. \n");
		input("Press any key to go back to menu ");
		menu();

def main():
	# Show the menu
	menu();

def menu(x=0):		
	if(x==0):

		newPage();
		print("\n 'list' to list all posts");
		print("\n 'create' to create a new post ");
		print("\n 'delete' to delete a post ");
		print("\n 'edit' to edit a post");
		line();
		print("\n 'render' to render site ");
		print("\n 'push' to push site to git repository");
		line();

		#get input from user
		selection = input("Enter your selection : ");
		#list of valid commands
		validSelection = ['list','create','delete','edit','render','push'];

		if(selection in validSelection):
			if(selection == "list"):
				listPost();
			if(selection == "create"):
				createPost();
			if(selection == "delete" ):
				deletePost();
			if(selection == "edit"):
				editPost();
			if(selection == "render"):
				render();
			if(selection == "push"):
				push();
		else:
			print("\n Invalid Selection ");
			time.sleep(0.75);
			menu(0);

# Main Interface
if(config.is_file()):
	print("Installation found. \n")
	main();
else:
	print("No Installation found \n")
	x = input("Do you want to start a fresh install ? (y/n) ")

	if(x == "y" or x == "Y"):
		install();
	elif(x == "n" or x == "N"):
		print("Terminating Installation Process. ")
		sys.exit()
	else:
		print("Invalid Selection. \n")
