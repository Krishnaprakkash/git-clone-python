import argparse #Library to read command line arguements
import configparser #Reads and writes config files in desired file formar
from datetime import datetime #Date and Time library
import grp, pwd #Read Groups and Users database respectively from UNIX
from fnmatch import fnmatch #Matching filenames
import hashlib #Hashing algorithms for securuity
from math import ceil #Ceil function to round up
import os #For path joins 
import re #For simple regular expressions
import sys #To access command line arguements
import zlib #Compression library

argparser = argparse.ArgumentParser(description="Simple Content Tracker")
 #Subparsers handle sub-commands like init, push..
argsubparsers = argparser.add_subparsers(title="Commands", dest="command") #Passes the name of the chosen subparser as string to variable command
argsubparsers.required = True #Makes a sub-command mandatory i.e. git COMMAND, required

def main(argv = sys.argv[1:]): #Reads command line argument and passes it as function paramter
    args = argparser.parse_args(argv) #Parses command line arguement from parameter
    match args.command: #Matches the parsed subcommand to one of the resprective bridge fucntion
        case "add"          : cmd_add(args) 
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")

class GitRepository (object): #Initiate Repo on local files
    """A git repository"""

    worktree = None #Location of files meant to be in version control live
    gitdir = None #Git directory inside workstree
    conf = None #Path of config file

    def __init__(self, path, force=False): #Pass path of directory to init repo in, force disables all checks
        self.worktree = path #Initialize worktree in the given path
        self.gitdir = os.path.join(path, ".git") #Set gitfir to look inside the worktree for a git directory

        if not (force or os.path.isdir(self.gitdir)): #If checks enabled and provided path doesnt have a git directort inside, flagged as not a git repo
            raise Exception(f"Not a Git repository {path}")

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser() #Initializes a config file reader using configparser
        cf = repo_file(self, "config") #Scans the config file into cf

        if cf and os.path.exists(cf): #if config file not empty and if config file path exists
            self.conf.read([cf]) #Reads config file using configparser

        elif not force: #If checks enabled and no config file
            raise Exception("Configuration file missing")

        if not force: #Checks enabled
            vers = int(self.conf.get("core", "repositoryformatversion")) #Get core repo version from config file
            if vers != 0: #If version not 0, as valid repo init should have version = 0
                raise Exception("Unsupported repositoryformatversion: {vers}")
            
def repo_path(repo, *path): #Path can be called with multiple components as separate arguments, recieved as a list
    """Compute path under repo's gitdir."""
    return os.path.join(repo.gitdir, *path) #Joins gitdir to the repo path

def repo_file(repo, *path, mkdir=False):
    """Same as repo_path, but create dirname(*path) if absent.  For
example, repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD\") will create
.git/refs/remotes/origin."""

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""

    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception(f"Not a directory {path}")

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


