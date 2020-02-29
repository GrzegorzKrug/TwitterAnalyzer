# TwitterAnalyzer

Application for analyzing and processing text information in tweets using Machine learning techniques.


## Install Package in editable state
Download files. 
Excecute command in root of project to install it from `setup.py`.

```pip install -e .```

or 

```pip3 install -e .```

## Application Status (Current plan, can be change any time)

#### API (4 / 7)

- [x] Verify authorization
- [x] Collect tweets from main page
- [ ] Collect comments from tweets
- [ ] Collect reactions on tweets
- [x] Post
	- [x] Tweets
	- [x] Tweets with images
- [ ] ~~Collect user followers (different than me)~~ not required atm
- [x] Collect user tweets (by statusid)
- [ ] Collect user comments
- [ ] ~~Background Queue for requests (twitter limit)~~ not here, in Analyzer
	

#### Analytic Tools (1 / 4)

- [x] Write Read to file
	- [x] Hold Temporary Tweets
	- [x] Load Tweets
	- [x] UTF-8 Support 
	- [x] Cleanup csv
	- [x] Rearrange csv	
	- [x] Save DF
- [ ] Collect Samples
    - [ ] Random walk
    - [ ] Snowballing
    
- [ ] ML Analysis of Tweets
	- [ ] Count Comments / Reactions
	- [ ] Normalize Tweets
		- [ ] Lowercase text
	- [ ] Analysis influence in time
		- [ ] Same id post
		- [ ] RT impact
	- [ ] Analysis Followers/Friends Tweets
		- [ ] Analysis random peoples being active in tweets
		- [ ] Suggest following new 
		- [ ] Suggest stop following 
		- [ ] Inform about friends attitude
	- [ ] Classify Tweets (3 Filters of Sokrates)
		- [ ] Good
		- [ ] Truth
		- [ ] Useful
	- [ ] Sort DF (? is this necessary ?)
	- [ ] Train model for predictions
		- [ ] Start making cool stuff
		- [ ] Enjoy
- [ ] Show Tweets
	- [ ] Decision model
	
#### GUI (3 / 8)

- [ ] Buttons
	- [x] Login, Status, Load CSVs
	- [ ] More Buttons
	- [ ] Download more tweets
- [x] Display log Console
- [x] Display CSV File Tree		
- [ ] Threading background
	- [x] Background requests
	- [x] Threads status, Checking, removing reference (release memory)
	- [ ] Threads feedback
- [ ] Filter tweets / Dataframe
	- [x] language
		- [x] English
		- [x] Polish
		- [x] Other with input parameter
	- [ ] user_id
	- [x] post_id
	- [x] by time range
		- [x] Date Posted
		- [x] Tweet age
	- [x] Find used words in text
	- [ ] Find exact text
	- [ ] Filter by other parameter	
- [x] Display tweets / Dataframe
	- [x] Display single tweets
	- [x] Browse tweets in current data frame
- [ ] Display Tweet activity
	- [ ] show comments quantity
	- [ ] show classification prediction
- [ ] Manage CSV files
	- [x] Loading selected CSV
	- [x] Save current DF to file
	- [ ] Merge without duplicates
- [ ] Auto Arrange tweets into files
	- [ ] Combine CSV  groups
		- [x] Combine selected
		- [ ] Auto Combine/Filter by Lang
		- [ ] Auto Combine/Filter by User
		- [ ] Popular
		- [ ] Other features
	- [ ] Remove
		- [ ] Old
		- [ ] prioritize new files if limit is reached. (1GB ? defined by user)
		- [ ] already used
		- [ ] Small
		- [x] With low tweet amount

#### Application 
- [x] Venv compatibility
	- [x] Installing modules
	- [x] Importing
	- [x] Setup.py
	- [x] Requirements.txt
			
