#!/usr/bin/python3
import json
import os
import cgi
import subprocess
import ffmpeg
import platform

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
        
location = './'
files_in_dir = []

print ('Content-Type: application/json\n\n')


# r=>root, d=>directories, f=>files
for r, d, f in os.walk(location):
   for item in f:
      if '.MP4' in item:
          videopath =  os.path.join(r, item)
          creationDate = creation_date(videopath)
          filename = item
          thumbnail = filename[:-4] + ".png"
          thumbnailpath = os.path.join(r, thumbnail)
          print("videopath: ", videopath)
          print("created date", creationDate)
          try:
              vid = ffmpeg.probe(videopath)
              print(vid['streams'])
              duration = round(float(vid['streams'][0]["duration"]))
              if duration > 10:
                jsonobj = {"videopath": videopath, "filename": filename, "thumbnailpath": thumbnailpath, "thumbnail": thumbnail, "created": creationDate, "duration": duration}  
                print("videopath: ", videopath)
                if not os.path.exists(thumbnailpath):
                    print("not exist")
                    command = "ffmpeg -i " + videopath + " -ss 00:00:10.000 -vframes 1 " +  thumbnailpath
                    subprocess.call(command, shell=True)
                    print("created thumbnail")
                else:
                    print("thumbnail already")
#                 subprocess.call("chmod 777 " + thumbnailpath, shell=True)    
                files_in_dir.append(jsonobj)
    
          except:
            print("error ffmpeg.probe")
jsondata = {"items": files_in_dir}
print(jsondata)


#print (json.dumps(jsondata, indent=4))   
with open("videos.json", "w") as outfile:
    json.dump(jsondata, outfile, indent=4)
# ~ for item in files_in_dir:
   # ~ print("<p>file in dir: ", item, "</p>")
   
   
