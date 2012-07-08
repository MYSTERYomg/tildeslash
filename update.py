#!/usr/bin/env python
#This fetches the latest files from the repo and puts them in the given folder
from __future__ import print_function
from urllib import urlopen
from argparse import ArgumentParser
import json, os, syslog

if __name__ == "__main__":
    #Get options
    parser = ArgumentParser(usage="update.py")
    parser.add_argument("-c", "--cron", dest="runSilent",
                help="run in cronjob (silent) mode", action="store_true", default=False)
    parser.add_argument("-d", "--dir", dest="directory",
                help="directory to save files to, default ~/", default=os.getenv("HOME"))

    args = parser.parse_args()

    log = print

    if args.runSilent:
        log = syslog.syslog

    def silentLog(msg):
        syslog.syslog("[dotfiles-update %s] %s" % (os.path.basename(os.getcwd()), msg))

    #Confirm, for safety's sake
    if not args.runSilent:
        yesNo = raw_input("Are you sure? (y/N) ")
        if yesNo != "y":
            log("Aborting.")
            os.sys.exit()

    #Get the path for the files on BitBucket
    revisionHash = json.loads(\
    urlopen("http://api.bitbucket.org/1.0/repositories/Yoplitein/tildeslash/changesets")\
                                                    .read())["changesets"][-1]["node"]
    baseURL = "https://bitbucket.org/Yoplitein/tildeslash/raw/" + revisionHash + "/"

    fileNames = [".bash_logout", ".bash_profile", ".bashrc", ".vimrc", "bin/afk"]

    #Make sure we're in the home directory
    os.chdir(args.directory)

    #Make sure ~/bin exists
    if not os.path.exists("bin"):
        os.mkdir("bin")

    #Write the files
    for fileName in fileNames:
        file = open(fileName, "w")
        fileContents = urlopen(baseURL + fileName).read()
        file.write(fileContents)
        file.flush()
        file.close()
        log("Wrote %s to disk." % fileName)

    log("Done.")