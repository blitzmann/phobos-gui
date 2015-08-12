# phobos-gui
This is a simple GUI wrapper for Phobos, an EVE Online client data dumper used for pyfa. Data is dumped into JSON files, which can then be manipulated with vertually any language or program that supports it. It's pretty straightforward. Once you select a valid EVE client directory and data dump directory, those paths will be saved for future use. Reverence will automatically find the client and shared resource directories, but in the off-chance that it incorrectly detects them, you can specify those as well.

This has only been tested on Windows, but will priobably work for Linux and OS X as well. It's also been tested only for TQ data, but whatever server works in Reverence should work here.

### Dependencies

* Python 2.7
* [Reverence](https://github.com/ntt/reverence)
* Phobos is shipped in the zipfile `Phobos.zip`

### How to use
Self-contained distributables are not compiled (yet). You must run this through a python interpreter with Reverence installed:

    python start.py

### Screenshots

![capture](https://cloud.githubusercontent.com/assets/3904767/9237455/ed78719c-4118-11e5-84e4-bb60d2950535.PNG)

![capture](https://cloud.githubusercontent.com/assets/3904767/9237438/d58e964c-4118-11e5-8ce6-6d981b577932.PNG)
