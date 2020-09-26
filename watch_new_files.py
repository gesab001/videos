import inotify.adapters

i = inotify.adapters.Inotify()
 
i.add_watch('/media/pi/Transcend/goprosync/')
 
for event in i.event_gen():
    if event is not None:
        (header, type_names, watch_path, filename) = event
 
        _LOGGER.info("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                     "WATCH-PATH=[%s] FILENAME=[%s]", 
                     header.wd, header.mask, header.cookie, header.len, type_names, 
                     watch_path, filename)
