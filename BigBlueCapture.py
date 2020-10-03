import os
import glob
from splinter import Browser
from pyvirtualdisplay import Display
import toml
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def getDisplayNumber():
    """ Get the id of the newly created virtual display.
    
        For each virtual display an entry is made in /tmp/.X11-unix/
        containing the display number. The last modified entry is fetched.
    """
    displayNumber = max(glob.glob('/tmp/.X11-unix/*'), key=os.path.getmtime)
    displayNumber = displayNumber.split('/')
    return displayNumber[3].split('X')[1]


def record(general, duration, did, ext):
    
    resolution = general['resolution']
    fps = general['fps']
    
    print('Start recording for: ' + ext)
    pipeline = 'ffmpeg -video_size {0}x{1} -framerate {2} -f x11grab -i :{3}.0 -f pulse -ac 2 -i default -t {4} {5}.mkv'.format(
        resolution[0], resolution[1], fps, did, duration, ext)
    p = subprocess.Popen(pipeline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    print('Recording finished.')
    out = p.communicate()[0]
    
    return out
    

def run(general, session, did):
    url = session['url']
    browser = Browser()
    browser.visit(session['url'])
    idx = url.find('/gl/') # BBB Greenlight
    fname = url[idx:len(url)] + "[join_name]"
    browser.fill(fname, general['name'])
    browser.find_by_id('room-join').click() # Join BBB session
    
    now = datetime.now()
    ext = session['prefix']+'-'+now.strftime("%d%m%Y-%H%M")
    
    out = record(general, session['duration'], did, ext)
    browser.quit()
    
    return out
    

if __name__ == "__main__":
    # execute only if run as a script
    
    config = toml.load("config.toml")
    general = config['general']
    sessions = config['sessions']
    
    print("Create and start virtual display")
    display = Display(visible=general['visibility'], size=(general['resolution'][0], general['resolution'][1]))
                      
    display.start()
    
    print("Fetch virtual display id")
    did = getDisplayNumber()
    
    print("Create schedule")
    scheduler = BlockingScheduler()
    
    print("Press CTRL+C to terminate application.")
    
    try:
        for session in sessions:
            hour = int(sessions[session]['time'].split(":")[0])
            minute = int(sessions[session]['time'].split(":")[1])
            scheduler.add_job(run, 'cron', day_of_week=sessions[session]['day'], 
                              hour = hour, minute = minute, args = [general, sessions[session], did])
    
        scheduler.print_jobs()
        scheduler.start()
    except KeyboardInterrupt:
        print("Application terminated. Virtual display stopped.")
        display.stop()
        
