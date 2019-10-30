# TwitterAnalyzer

Python Application for improving twitter content and quality of usage

## Application Status (Current plan, can be change anytime)

#### API (4 / 7)

- [x] Verify authorization
- [x] Collect tweets from main page
- [ ] Collect comments from tweets
- [ ] Collect reactions on tweets
- [x] Post
	- [x] Tweets
	- [x] Tweets with images
- [ ] ~~Collect user followers (diffrent than me)~~ not required atm
- [x] Collect user tweets (by statusid)
- [ ] Collect user comments
- [ ] ~~Background Queue for requests (twitter limit)~~ not here, in Analyzer
	

#### Analytic Tools (1 / 3)

- [x] Write Read to file
	- [x] Hold Temporary Tweets
	- [x] Load Tweets
	- [x] UTF-8 Support 
	- [x] Cleanup csv
	- [x] Rearange csv	
	- [x] Save DF
- [ ] Analzye Tweets
	- [ ] Count Comments / Reactions
	- [ ] Normalize Tweets
		- [ ] Text lowercase
	- [ ] Analyze changes in time
		- [ ] Same id post
		- [ ] RT impact
	- [ ] Analyze Followers/Friends Tweets
		- [ ] Analyze random peoples being active in tweets
		- [ ] Suggest following new 
		- [ ] Suggest stop folloing 
		- [ ] Inform about friends attitude
	- [ ] Classify Tweets (3 Filters of Sokrates)
		- [ ] Analyze word count
		- [ ] Good
		- [ ] Truth
		- [ ] Useful
	- [ ] Train model for predictions
- [ ] Show Tweets
	- [ ] Decision model
	
#### GUI (2 / 7)

- [ ] Buttons
	- [x] Login, Status, Load CSVs
	- [ ] More Buttons
- [x] Display log Console
- [x] Display CSV File Tree		
- [ ] Threading background
	- [x] Background requests
	- [ ] Threads status
	- [ ] Threads feedback
- [ ] Filter tweets Dataframe
	- [ ] Filter by key and param
		- [ ] user_id
		- [ ] post_id
		- [ ] by time range
			- [ ] Time collected
			- [ ] Tweet borned
	- [ ] Filter by words included
	- [ ] Filter 
- [ ] Display tweets / Dataframe
	- [ ] show comments quantity
	- [ ] show classification prediction
- [ ] Manage CSV files
	- [x] Loading selected CSV
	- [x] Save current DF to file
	- [ ] ReArange
		- [ ] Combine CSV  groups
			- [ ] By Lang
			- [ ] By User
			- [ ] Popular
			- [ ] Other features
	- [ ] Remove
		- [ ] Old
		- [ ] Used
		- [x] Small
	