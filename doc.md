# Getting Started with StarData with Python
This note might be helpful if you're wanting to make use of the StarData dumped_replays data using Python.


## Installation
Note: This was tested on a Mac OS X.

### 1. Install Torch

i) Note: in a terminal, run the commands WITHOUT sudo:

	`git clone https://github.com/torch/distro.git ~/torch --recursive`

	`cd ~/torch; bash install-deps;`
	
	`./install.sh`

ii) Add Torch environment variable in .bash_profile:

	`vi ~/.bash_profile`

	In .bash_profile, add the following line:

	`. <path to torch-activate>`


	Example:

	`. /Users/user/torch/install/bin/torch-activate`


iii) To check that this works, try call 'th' to launch torch from anywhere. Torch should launch.
	'th'


### 2. Install Dependencies.

i) zeromq (I used homebrew to install this).

	`brew install zeromq`

ii) zstd
	
	`git clone https://github.com/facebook/zstd`

	`cd zstd`
	
	`make install`


### 3. Install TorchCraft.

	`git clone https://github.com/TorchCraft/StarData`
	
	`git submodule update --init`
	
	`cd TorchCraft`
	
	`pip install .`


### Some Troubleshooting Errors:

1. If you get a fatal error that a particular header file (.h) is not found, for example, `fatal error: 'zmq.h'` file not found, this could either be due to:

	i)  You haven't installed that dependency yet, 

	ii) Python has trouble locating the file (possibly need to add the filepath to .bash_profile).



## Downloading the Data

The data is hosted on Amazon S3. Here's a suggestion of steps to download the data by creating an S3 Account.

### 1. Create an Amazon S3 account:

i. Go to: https://console.aws.amazon.com/iam/home?#security_credential . This requires setting a new account, and entering address information, and billing information. There is a Free Tier account with limits on S3 storage (5GB) and monthly data transfer out (15GB).

ii. Lookup access key and secret access key in your AWS account -> your name -> My Security Credentials.

iii. Set credentials: run 'aws configure' and specify your access key, secret access key, and region from step ii. Example for region: mine was us-east-1.


### 2. Install the AWS command line interface

`sudo easy_install awscli`


### 3. Download the data!

`aws s3 sync s3://stardata/dumped_replays .`

The total download size for the dumped_replays is 365.6 GB, which contains 19 zipped folders of about 20GB each, named from 0 to 19. Also included are three .list files specifying which replay files are in the train, validation and test sets. 

The replay files have the extension .tcr. Some files are anmed generically like 'bwrep_zz20m.tcr', where bwrep could refer to Brood War Replay. Other files are more informatively named, like 'IC_PvP_IC417320.tcr', which could refer to a Protoss vs Protoss match, 'IC_TvZ_IC311132.tcr', which could refer to Terran vs Zerg, and 'TL_PvT_GG6995.tcr' referring to Protoss vs Terran, as some examples. 


## Running their base cpp scripts

`cd` into the StarData folder. Before running the cpp files from StarData, run `make`.

To run extract_stats.cpp, assuming you have downloaded the dumped_replays data, run:

`./extract_stats "path to replay data folder" "folder number"`

As an example:

`./extract_stats /Users/user/Desktop/StarCode/replay_data 0`

Troubleshooting:

If you get an error "Need two arguments, source file path and which fold" and were wondering what "fold" refers to, it means folder number.


## A First Python Script 
'''from torchcraft import replayer
rep = replayer.load("replay_data/0/bwrep_0b8dp.tcr")
for i in range(len(rep)):
	frame = rep.getFrame(i)
	print("On frame " + str(i))
	for team in frame.units:
		for u in frame.units[team]:
			print(u.id, u.x, u.y)'''

Since we are working with the replay data and using Python, the script relevant to this use case is pyreplayer.cpp. Relevant files for reference:

1. TorchCraft/docs/user/replayer.md
2. TorchCraft/py/pyreplayer.cpp

As a side note: TorchCraft replayer (replayer.cpp) is a C++ library with Lua bindings. The Python wrapper pyreplayer.cpp uses pybind to create Python bindings of this C++ library. (As an aside, pybind was started by a [Professor at EPFL](http://rgl.epfl.ch/people/wjakob).


## References

1. Andrew Silva has also documented his experience with setting up StarData, with well elaborated walktroughs: https://github.com/andrewsilva9/stardata_analysis.

2. StarData dataset: https://github.com/TorchCraft/StarData

3. TorchCraft: https://github.com/TorchCraft/TorchCraft



