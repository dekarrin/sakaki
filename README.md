## SakakiLauncher
A game/application launcher built on pygame that uses external macro applications to remap controls.

SakakiLauncher was created on the principle that configuring a launcher is not something that should be difficult. It is not as pretty as some other launchers, but configuring it is as easy as editing plaintext files. In addition, Sakakilauncher provides a non-intrusive way to handle control remapping that leaves the application itself untouched.

Another goal of SakakiLauncher is to be fully cross-platform. As of this writing, this is not the case. Some features only work correctly on one platform or the other. This will be corrected in future versions.

### Compatibility
SakakiLauncher is currently compatible only with Windows, due to its reliance on AutoHotkey for control remapping. It has been tested only on Windows 7.

### Installation
As a python application, SakakiLauncher does not have a particularly difficult install process. Download/install the dependencies, and then place SakakiLauncher into whatever location is desired. Then configure the launcher. It can then be started it by executing `sakaki.py` with python in the root directory of the launcher.

#### Dependencies
The following external programs/libraries are needed to execute SakakiLauncher. The versions given are the minimum versions; later ones also should work, though Python 2 is required for compatibility with Pygame.

* Python 2.7 or later (http://www.python.org/downloads)
* Pygame 1.9 or later (http://www.pygame.org/download.shtml)
* psutil 3.1 or later (https://pypi.python.org/pypi/psutil/#downloads)
* AutoHotkey 1.1 or later (http://www.autohotkey.com)
