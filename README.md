# BigBlueCapture

BigBlueCapture is a tool for automated and scheduled joining and recording of BigBlueButton sessions. Using TOML it is possible to specify when and at what time the recordings should take place. BigBlueCapture creates a virtual display where a BigBlueButton session is joined and recorded.

# Getting started

Get the latest version of BigBlueCapture by cloning it 
```git clone git@github.com:k0ssmann/BigBlueCapture.git ```
modify `conf.toml` after your needs and run `python BigBlueCapture.py`.

## Usage

Configuring and adding of BigBlueButton sessions is done in the `conf.toml`.

### General options
    
    - visibility: 0 - Hide virtual display, 1 - Show virtual display (requires Xephyr.)
    - resolution: Resolution of the virtual display in the format [width, height]
    - fps: frames per second
    - name: name used in BigBlueButton sessions

### Sessions
BigBlueButton sessions can be added by adding them to the sessions section. Add a new subsection `sessions.$Session` where `$Session` is the name of a BigBlueButton session with following options

    - url: url of BigBlueButton session
    - day: the day session should be recorded. Can take the values `mon`,`tue`,`wed`,`thu`,`fri`,`sat` or `sun`.
    - time: the time session should be recorded in the format `HH:MM`
    - duration: how long a session should be recorded in seconds.
    - prefix: prefix of file name
    - saveDir: path where recordings should be saved.
    
### Platforms

* GNU/Linux
    
### Dependencies

* python >= 3.6
* xvfb
* xserver-xephyr (optional)

BigBlueCapture requires the following python-packages:

* splinter
* pyvirtualdisplay
* toml
* apscheduler
    
### Known Issues

* Sounds outside the virtual display are recorded, too. 

