from datetime import datetime
from os import listdir
from os.path import isfile, join

#variable declr.
count = 0
s = '00:00:00,000'
e = '00:00:00,000'

#the only manual work! Find all time instances when subs begin for all episodes
orig = ['00:50:32,100','01:44:25,750','02:38:08,100','03:32:58,200','04:25:50,010','05:08:35,850','05:51:27,010','06:48:22,950']
mypath = r'path_to_directory_with_SubtitleFiles'

#find all files in the SUBTITLES directory
files = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and (f.__contains__('.srt')))]

#start from 1 to leave out first file; make sure the files are sorted by episodes
for file in range(1, len(files)):
  
  with open(join(mypath, files[file])) as fp:
    Lines = fp.readlines()
  
  diff = datetime.strptime(orig[count], '%H:%M:%S,%f') - datetime.strptime(Lines[1][:12].strip(), '%H:%M:%S,%f')
  count = count + 1
  
  for line in range(0, len(Lines)):
    #find lines with the '-->' substring
    if Lines[line].__contains__('-->'):

      #finding the current time values
      start_time = datetime.strptime(Lines[line][:12].strip(), '%H:%M:%S,%f')
      end_time = datetime.strptime(Lines[line][17:].strip(), '%H:%M:%S,%f')
      
      cons = ''
      
      if(len(str(diff + start_time)[12:-3])>10):
        cons = str(diff + start_time)[12:-3]
      else:
        cons = str(diff + start_time)[12:]+'.000'
      
      if(len(str(diff + end_time)[12:-3])>10):
        cons = cons + ' --> ' + str(diff + end_time)[12:-3]+'\n'
      else:
        cons = cons + ' --> ' + str(diff + end_time)[12:]+'.000\n'

      #replace the line with updated time values
      Lines[line] = cons
  
  #append all subtitles to the first episode's subs    
  with open(r'path_to_first_episode_subtitlefile.srt', 'a+') as fp: 
    fp.write('\n')
    fp.writelines(Lines)

