
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
	
#### GUI (4 / 9)

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
- [ ] Filter tweets
    - [ ] Inverted filtration
	- [x] language
		- [x] English
		- [x] Polish
		- [x] by input
	- [ ] user_id / username
	- [x] post_id
	- [x] by time range
		- [x] Date Posted
		- [x] Tweet age
	- [x] Find words and phrases 
	    - [x] in text
	    - [x] in every field or key
	- [x] Find tweets with non empty fields
- [x] Display tweets
	- [x] Display single tweets
	- [x] Browse tweets in current data frame
	- [x] Pretty display
	    - [x] Short users
	    - [x] Hide empty fields
	    - [x] Quoted tweets are prettier
- [ ] Display Tweet activity
	- [ ] show comments quantity
	- [ ] show classification prediction
- [x] Manage CSV files
	- [x] Load selected CSV
	- [x] Save current DF to file
	- [x] Merge files
- [ ] Auto Arrange files
	- [ ] Combine CSV  groups
		- [x] Combine selected
		- [x] Combine without duplicates
		- [ ] Auto Combine/Filter by User
		- [ ] Keep Popular
		- [ ] Other features
	- [ ] Delete / AutoClean
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
			