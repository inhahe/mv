import win32api, win32con, os, sys, shutil

orig, dest = sys.argv[1:]

pj = os.path.join
ps = os.path.split

failed = []

fileexists = "ask"
direxists = "ask"

def walk(origpath, origfile, destpath, destfile):
  global direxists, fileexists
  destfull = pj(destpath, destfile)
  origfull = pj(origpath, origfile)
  print origfull
  try:
    win32api.SetFileAttributes(origfull, win32con.FILE_ATTRIBUTE_NORMAL)
  except: pass
  try:
    if os.path.isdir(origfull):
      if os.path.exists(destfull):
        if direxists == "ask":
          while 1:
            print "'"+destfull + "' already exists.  Merge all directories? y/q(quit):",
            i = raw_input().lower().strip()
            if i.startswith('y'):
              direxists = "always"
              break
            elif i.startswith('q'):
              raise SystemExit
        elif direxists=="always":
          print "..already exists"
      else:
        os.mkdir(destfull)
      for fn in os.listdir(origfull):
        walk(origfull, fn, destfull, fn)
      os.rmdir(origfull)
    else:
      if os.path.exists(destfull):
        if fileexists=="ask":
          while 1:


            print destfull
            print os.path.isdir(destfull)

            print "'"+destfull + "' already exists.  Overwrite?  y/n/a(always)/v(never)/q:",
            i = raw_input().lower().strip()
            if i.startswith('y'): 
              shutil.copy(origfull, destfull)
              break
            elif i.startswith('n'):
              break
            elif i.startswith('a'):
              filexists = "always"
              shutil.copy(origfull, destfull)
              break
            elif i.startswith('v'):
              fileexists = "never"
              break
            elif i.startswith('q'):
              raise SystemExit
        elif fileexists=="always":
          shutil.copy(origfull, destfull)
        elif fileexists=="never":
          print "..already exists"
      else:
        shutil.copy(origfull, destfull)
        os.remove(origfull)
  except:
    failed.append((origfull, sys.exc_type.__name__, sys.exc_value))
    print "..failed: %s: %s" % (sys.exc_type.__name__, sys.exc_value)

walk("", orig, "", dest)

if failed:
  print
  print "Could not copy and/or remove the following files:"
  print
  for f in failed:
    print "'%s': %s: %s" % f





