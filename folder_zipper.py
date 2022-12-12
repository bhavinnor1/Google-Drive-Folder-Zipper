
# importing required modules
from subprocess import getoutput
from IPython.display import display, clear_output, HTML
from zipfile import ZipFile
import zipfile 
import os
from google.colab import drive

from time import time, sleep

#drive.mount('/content/drive')  # access drive
# need to install xattr
#!apt-get install xattr > /dev/null

#save zip location 


def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths       

def main():
    # path to folder which needs to be zipped
    fullname="/content/drive/MyDrive"
    exclude_list=[]
    exclude_files=False
    
    try:
       folders = os.listdir("/content/drive/MyDrive")
    except:
       print ("Google Drive Not Mounted\nMounting GDrive...")
       drive.mount("/content/drive")
       folders = os.listdir("/content/drive/MyDrive")
       
    n=1
    alist=[]
    for name in folders:
       #if "kayoanime" in (name.split("/")[-1]).lower():
          print (str(n)+"> " + name.split("/")[-1])
          n+=1
          alist.append("/content/drive/MyDrive/"+name)
          
    
    directory = input("\nFolder: ")
    dir_split = directory.strip().split(" ")
    if len(dir_split)==2 and len(dir_split[0])>0 and len(dir_split[1])==1:
       if dir_split[1]=="e":
          clear_output()
          print ("Folder:",directory,"\n[Exclude]")
          if dir_split[0].isdigit():
             directory=alist[int(dir_split[0].strip())-1]
          else:
             directory=dir_split[0].strip()
          print (directory)
          lssdir=os.listdir(directory)
          print ("\n")
          lssdir.sort()
          #print (lssdir)
          ziplist=[]
          n=1
          for name in lssdir:
             print (str(n)+"> " + name.split("/")[-1])
             n+=1
             ziplist.append(directory+"/"+name)
          exclude=input('\nEnter index of files/folders you\nwant to exclude\n(Seperated by commas ","):\n')
          exclude=exclude.strip().split(",")
          exclude_list=[]
          for i in exclude:
             long_list=i.strip().split('-')
             if len(long_list)==2:
                frm=int(long_list[0].strip())
                to=int(long_list[1].strip())
                for j in range (frm-1,to):
                   exclude_list.append(ziplist[j])
             elif i!="":
                exclude_list.append(ziplist[int(i.strip())-1])
          exclude_files=True
    elif directory.strip().split(" ")[0].isdigit():
       clear_output(wait=True)
       print("\nFolder:",directory)
       directory=alist[int(directory.strip().split(" ")[0].strip())-1]
       print (directory.split("/")[-1])

    # calling function to get all file paths in the directory
    files_add=[]
    #print ("\n".join(exclude_list))
    if exclude_files==True:
       #print ("\n".join(exclude_list))
       #sleep(20)
       path_list=[]
       #print (directory)
       for i in os.listdir(directory):
           path_list.append(directory+"/"+i)
       for i in path_list:
           if i not in exclude_list:
              #print (i)
              if os.path.isdir(i):
                 ll=get_all_file_paths(i)
                 for j in ll:
                    files_add.append(j)
              else:
                 files_add.append(i)
       #print("\n\nFiles_add: ","\n".join(files_add))
       file_paths=files_add
    else:
       file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    clear_output()
    
    print(directory.split("/")[-1])
    print('\nFollowing files will be zipped:')
    #print(file_paths[0].split("/")[-1]+"\nto...\n"+file_paths[-1].split("/")[-1]+"\n")
    print("\n".join(file_paths))
    print("Total:-",len(file_paths),"files.\n")

    # writing files to a zipfile
    savehere=input("Save Location:- ")
    nameofzip=directory.split("/")[-1]
    savedir=savehere
    ls=os.listdir(savehere)
    print (ls)
    print (nameofzip)
    same_count=0
    for i in ls:
       if i.find(nameofzip):
          
          same_count+=1
    if same_count>0:
       nameofzip=nameofzip.split(".")[0]+f" ({same_count}).zip"
    else:
       nameofzip=nameofzip+".zip"
    
    if savehere[-1]!="/":
        savehere=savehere+"/"
    if os.path.isdir(savehere)==False:
        os.mkdir(savehere)
    fullname=savehere+nameofzip
    fc=0
    file_paths.sort()
    with ZipFile(fullname,'w') as zip:
        # writing each file one by one
   
        for file in file_paths:
            #if file not in exclude_list:
            zip.write(file, arcname=file.split(directory)[-1])
            #os.system('clear')
            clear_output(wait=True)
            
            print(nameofzip+" - [Zipping]\n")
            for i in range(0,len(file_paths)):
               print (str(i+1)+"> "+file_paths[i].split("/")[-1])
            print("Total:-",len(file_paths),"files.\n")
            fc+=1
            print("Zipping in progress... [" +str(fc)+"/"+str(len(file_paths))+"]")
            percent=(fc/len(file_paths))*100
            display (HTML (f'<progress width="9em" id="file" value="{round (percent,2)}" max="100"> {round(percent,2)}% </progress> {round(percent,2)}%'))

            #print("["+("-"*fc)+">"+(" "*(len(file_paths)-fc))+"]\n"+str(fc)+"/"+str(len(file_paths)))

            if file==file_paths[-1]:
                print ("Zipping Finished.")
            else:
                print(file.split("/")[-1])

            

    print('All files zipped successfully!')  
    print ("\nGenerating Link..")
    clear_output(wait=True)
    print (nameofzip+' - [link]')
    print ('Fetching link...')
    display (HTML('<style>body {  margin: 10px;  padding: 0;}.container {  width: 250px;  height: 20px;  margin: 0 auto;}.ball {  float:left;  width: 10px;  height: 10px;  margin: auto 10px;  border-radius: 50px;}    .ball:nth-child(1) {      background: #ff005d;      -webkit-animation: right 1s infinite ease-in-out;    }    .ball:nth-child(2) {      background: #35ff99;      -webkit-animation: left 1.1s infinite ease-in-out;    }    .ball:nth-child(3) {      background: #008597;      -webkit-animation: right 1.05s infinite ease-in-out;    }    .ball:nth-child(4) {      background: #ffcc00;      -webkit-animation: left 1.15s infinite ease-in-out;     }    .ball:nth-child(5) {      background: #2d3443;        -webkit-animation: right 1.1s infinite ease-in-out;    }    .ball:nth-child(6) {      background: #ff7c35;        -webkit-animation: left 1.05s infinite ease-in-out;     }    .ball:nth-child(7) {      background: #4d407c;       -webkit-animation: right 1s infinite ease-in-out;    }@-webkit-keyframes right {  0%   { -webkit-transform: translateY(-15px);   }  50%  { -webkit-transform: translateY(15px);    }  100% { -webkit-transform: translateY(-15px);   }}@-webkit-keyframes left {  0%   { -webkit-transform: translateY(15px);    }  50%  { -webkit-transform: translateY(-15px);   }  100% { -webkit-transform: translateY(15px);    }}@-moz-keyframes right {  0%   { -moz-transform: translate(-15px);   }  50%  { -moz-transform: translate(15px);    }  100% { -moz-transform: translate(-15px);   }}@-moz-keyframes left {  0%   { -moz-transform: translate(15px);    }  50%  { -moz-transform: translate(-15px);   }  100% { -moz-transform: translate(15px);    }}@keyframes right {  0%   { transform: translate(-15px);  }  50%  { transform: translate(15px);   }  100% { transform: translate(-15px);  }}@keyframes left {  0%   { transform: translate(15px);   }  50%  { transform: translate(-15px);  }  100% { transform: translate(15px);   }}</style><div class="container">  <div class="ball"></div>  <div class="ball"></div>  <div class="ball"></div>  <div class="ball"></div>  <div class="ball"></div>  <div class="ball"></div>  <div class="ball"></div></div>'))
    print (fullname)
    get_link(fullname)

def get_size(path):
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024*1024:
        return f"{round(size/1024, 2)} KB"
    elif size < 1024*1024*1024:
        return f"{round(size/(1024*1024), 2)} MB"
    elif size < 1024*1024*1024*1024:
        return f"{round(size/(1024*1024*1024), 2)} GB"


def get_link(file_path):
    shareable_link = get_shareable_link(file_path)
    #shareable_link = get_shareable_link(file_path)
    if 'local-' not in shareable_link:
          clear_output()
          print("Name: "+file_path.split("/")[-1])
          print("Location: "+file_path)
          size=get_size(file_path)
          print(f"Size: {size}")
          print("\nLink Fetched")
          print(f"Click Below 👇 to download [{size}]\n")
          return display(HTML(f"<center><a style='font-size:1.1em; background:#007FFF; color:white; text-decoration:none; padding:1em; border-radius: 5px;' href=https://drive.google.com/uc?export=download&confirm=no_antivirus&id={shareable_link} target=_blank>Download</a></center>"))
       
    while 'local-'==shareable_link[:6]:
       #sleep(5) 
       #clear_output()
       shareable_link = get_shareable_link(file_path)
       if 'local-' not in shareable_link:
          clear_output()
          print("Name: "+file_path.split("/")[-1])
          print("Location: "+file_path)
          size=get_size(file_path)
          print(f"Size: {size}")
          print("\nLink Fetched")
          print(f"Click Below 👇 to download [{size}]\n")
          return display(HTML(f"<center><a style='font-size:1.1em; background:#007FFF; color:white; text-decoration:none; padding:1em; border-radius: 5px;' href=https://drive.google.com/uc?export=download&confirm=no_antivirus&id={shareable_link} target=_blank>Download</a></center>"))
       #print (shareable_link)
       #print('trying to avoid local- issue...')
    #sleep(5)

def get_shareable_link(file_path):
  fid = getoutput("xattr -p 'user.drive.id' " + "'" + file_path + "'")
  # print (fid) # for debugging
  if "not found" in fid:
     !apt-get install xattr > /dev/null
     get_link(file_path)
  else:
     return fid
  return 'local-'




if __name__ == "__main__":
    main()
