# phobos-gui
This is a simple GUI wrapper for Phobos, an EVE Online client data dumper used for pyfa. Data is dumped into JSON files, which can then be manipulated with virtually any language or program that supports it. It's pretty straightforward. Once you select a valid EVE client directory and data dump directory, those paths will be saved for future use. Reverence will automatically find the client and shared resource directories, but in the off-chance that it incorrectly detects them, you can specify those as well.

This has only been tested on Windows, but will priobably work for Linux and OS X as well. It's also been tested only for TQ data, but whatever server works in Reverence should work here.

### Dependencies for running from source

* Python 2.7
* [Reverence](https://github.com/ntt/reverence)
* Phobos is shipped in the zipfile `Phobos.zip`

### Screenshots

![1](https://cloud.githubusercontent.com/assets/3904767/9255884/2857c1cc-41ba-11e5-9c2f-fb44091b2f96.PNG)
![2](https://cloud.githubusercontent.com/assets/3904767/9255885/2972f5b8-41ba-11e5-839c-1325e5f531e2.PNG)

