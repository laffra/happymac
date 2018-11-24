# HappyMac

![HappyMac Icon](http://chrislaffra.com/happymac/happymac.webp =150x)

  HappyMac features:
  - Automatically suspends background processes
  - Stops your CPU from heating up
  - Preserves battery life
  - Makes your Mac happy again

Visit [happymac.app](https://happymac.app) for a ready to install DMG of HappyMac.

# How it works
HappyMac is a status bar app for Mac. It looks like this when activated:

   ![HappyMac Icon](http://chrislaffra.com/happymac/menu3.png =250x)

The icon itself changes from *happy* to *unhappy* to *sweating* to *mad*, depending on the current load of your Mac. In the menu above, the machine is showing as *sweating*, as the overall CPU usage on the machine, including all available cores, is currently in between 51% and 75%.

The menu shows three categories of processes:
  - **Current App Tasks**: These are the processes that make up the *process* *family* of the currently active application. This includes the process that created the currently active window and all its parent processes up to the Launch process. Also included are all the child processes of the current process, their child processes, etc. 
  
  - **Background Tasks**: These are tasks that use up CPU even though they run in the background. Literally hundreds of tasks normally run in the background and they only become troublesome when they run hot. In the menu shown below, there are 4 background tasks, that together use up about 30% of one CPU, which is about 8% of the entire machine.
  ![HappyMac Icon](http://chrislaffra.com/happymac/menu4.png =400x)
  At any point in time you can decide to suspend any background task using the context menu, as is shown above. What happens is that the given task is suspended and moved to the suspended tasks. HappyMac also remembers this decision and will make sure the process is suspended any time it is not part of the foreground task family.
  - **Suspended Background Tasks**: Suspended tasks are those that are currently suspended by HappyMac. You can resume a suspended task by bringing the process to the foreground, assuming it has a UI. You can also manually resume a task using the context menu:
![HappyMac Icon](http://chrislaffra.com/happymac/menu5.png =400x)
Once a suspended process is activated, by using Cmd+Tab for instance, all the processes in its family are resumed. The logic for suspending and resuming is currently hardwired into HappyMac. 

To remove noise, active processes that use up less than 3% of CPU are not shown. Unlike the overall CPU represented by the status bar icon, a given task can use more than 100% of CPU. This is the case when a task uses more than one core of the machine. Most Macbooks have 4 cores and some even 6. It is quite uncommon for a process to use more than 100% of the CPU. Few processes use more than 2 cores. 

Just like the task bar icon, each individual task gets a different emoticon for each percentage of CPU it uses. The same scale is used. A happy process uses 25% CPU or less (of one core), an unhappy 50% or less, a sweating one 75% or less, and a mad one more than 75%.

### A Practical Example
Say we are developing an Android app and start up the Intellij IDE. From it, we launch the Android emulator. CPU goes up, as we can tell as it will not take long for the Macbook's fan to turn on. When we switch to another application, both the **idea** and **qemu-system-i386** tasks keep using CPU:

![HappyMac Icon](http://chrislaffra.com/happymac/menu6.png =300x)
Together, they use up more than two cores. Eventually, **idea** will slow down and not use any CPU anymore, but the second task (which is the Android emulator) keeps on using CPU, even when it is "not doing anything". With HappyMac, such processes can be automatically suspended. This is what the machine looks like with both processes suspended:
![HappyMac Icon](http://chrislaffra.com/happymac/menu7.png =300x)

Shown in blue above, my CPU is still kind of "unhappy". This is because CrashPlan and Carbon like to use up 30% of the CPU on average on my machine and this tends to go up higher when doing a large build. If I am low on battery, or connected over tether on my phone, you could decide to suspend things like backups temporarily and make your Mac really happy again:

![HappyMac Icon](http://chrislaffra.com/happymac/taskbar-happy.png =200x)

### Admin Tasks

Sometimes, you may want to suspend a process that does not belong to your current user account. In such a case, HappyMac will ask you to provide an admin or root password for your machine, so it can "sudo" suspend the process. The dialogue will look like this:

![HappyMac Icon](http://chrislaffra.com/happymac/admin.png =400x)

### Critical Tasks

Some Mac tasks are part of the operating system and have a critical function. One such example is *WindowServer*. It is the process that draws your display and handles events. If you suspend that process, the only recovery would be to shut down your mac by pressing the power button for 5 seconds. Process like WindowServer will not be suspended by HappyMac:
 ![HappyMac Icon](http://chrislaffra.com/happymac/windowserver.png =500x)

### Implementation

HappyMac is written in Python and uses [psutil](https://pypi.org/project/psutil/) to list all processes every two seconds, compute their CPU, compute the current foreground task family and resume it, if needed. Any previously suspended process that is now running in the background will be suspended automatically as well. If the status bar menu is open, it is redrawn to show the current state.

To draw the status bar menu and the dialogs shown above, [rumps](https://github.com/jaredks/rumps) is used.

The distribution, i.e., the DMG file, is created using 

### Development

Want to contribute? Great! Simply download this git repo and send a pull request.

### What is next?

It would be great to add more refined policies for suspending processes. Policies to consider:

  - Only suspend a background process when it uses more than 35%
  - Only suspend process X when I am on battery
  - When doing a build, don't do backups
  - When I am tethered to my phone, suspend process that use the network for more than X MB per minute
  - When the CPU is below 30% for a while, it is OK to run backups

### License
MIT


### Build HappyMac Yourself

You can build HappyMac yourself, or run "python src/happymac.py" from a local repo.

However, for daily use, we suggest you visit [happymac.app](https://happymac.app) and download the ready to install DMG of HappyMac.
