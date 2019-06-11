# import modules
import os
import urllib.request
from datetime import datetime
from datetime import timedelta

# editing Chris Micheal's original code to pull different files from bathyDuck
# UPDATED to python 3.7 by Sarah Trimble in 2019 - sarah.trimble.ctr@nrlssc.navy.mil

# folder where we want to put Argus images that we grab
OUTPUT_FOLDER = r"C:\Users\strimble\Projects\DirMinVar\ARGUS_data\year2015" ##change year
logFileName = os.path.join(OUTPUT_FOLDER, 'log_29min+125m.txt') ##change this name to suit your needs
with open(logFileName, 'w') as f:
    f.write("URLs / files not found: \n")

# hours of interest
hourTuple = (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22) ##change this to suit your needs

# url format of images on CIL server
top_level_url = ("http://cil-www.oce.orst.edu/argus02b/2015/cx/") #change year
url = ("http://cil-www.oce.orst.edu/argus02b/2015/cx/"+\
            "%(dayOfYear)s_%(mon)s.%(dayOfMonth)s/"+\
            "%(unixTime)s.%(day)s.%(mon)s.%(dayOfMonth)s_%(hour)s_29_01.GMT.%(year)s.argus02b.cx.vbar125.mat"
            ) ##change year, minutes, end of file name as needed to access files of interest

##change to your CIL username & password
auth_user = 'string'
auth_pass = 'string'

pass_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
pass_mgr.add_password(None, top_level_url, auth_user, auth_pass)
auth_handler = urllib.request.HTTPBasicAuthHandler(pass_mgr)
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)

if __name__ == '__main__':
    d = {}

    ##change to your date range of interest where (Year, Month, Day, Hour, Minute, Second) 
    minDate = curDate = datetime(2015,9,15,0,29,1)
    maxDate = datetime(2015,10,9,0,0,1)

    while curDate.timetuple().tm_yday < maxDate.timetuple().tm_yday:
        d["dayOfYear"] = curDate.strftime("%j")
        d["mon"] = curDate.strftime("%b")
        d["dayOfMonth"] = curDate.strftime("%d")
        d["year"] = curDate.strftime("%Y")
        d["day"] = curDate.strftime("%a")

        for curHour in hourTuple:
            curDate = curDate.replace(hour=curHour)
            d["hour"] = curDate.strftime("%H")
            d["unixTime"] = str(int((curDate - datetime(1970,1,1)).total_seconds()))
            folderName = ("%(dayOfYear)s_%(mon)s.%(dayOfMonth)s")
            ##change the below to match line 23
            fileName = ("%(unixTime)s.%(day)s.%(mon)s.%(dayOfMonth)s_%(hour)s_29_01.GMT.%(year)s.argus02b.cx.vbar125.mat")
            completeFolder = os.path.join(OUTPUT_FOLDER, folderName%d)
            outFileName = os.path.join(completeFolder, fileName%d)

            if not os.path.exists(completeFolder%d):
                print("Making directory", completeFolder)
                os.mkdir(completeFolder%d)

            try:
                if not os.path.exists(outFileName%d):
                    print('...Looking for ' + url % d)
                    urllib.request.urlretrieve(url%d, outFileName%d)
                    print('File saved...')
            except:
                print('No file at that url...')
                with open(logFileName, 'a') as f:
                    f.write(url%d + "\r\n")

        curDate += timedelta(1)

    #clear so rerun of script resumes at start
    del curDate
    del curHour
