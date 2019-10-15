# TwitterAnalyzer

### Application Status (Current plan, can be change anytime)

[ ] - Application to Analyze Twitter Content
	[ ] - API
		[x] - Login
		[x] - Collect tweets from main page
		[ ] - Collect comments from tweets
		[ ] - Collect reactions on tweets
		[ ] - ~~Collect user followers (diffrent than me)~~ not required atm
		[ ] - Collect user tweets (diffrent than me)
		[ ] - Collect user comments (diffrent than me)
	[ ] - Analytic Tools
		[ ] - Write Read to file
			[x] - Hold Temporary Tweets
			[x] - Load Tweets
			[x] - UTF-8 Support 
			[ ] - Cleanup
			[ ] - Rearange			
		[ ] - Analzye Tweets
			[ ] - Count Comments / Reactions
			[ ] - Analyze change in time
				[ ] - Same id post
				[ ] - RT impact
			[ ] - Classify Tweets (3 Filters of Sokrates)
				[ ] - Analyze word count
				[ ] - Good
				[ ] - Truth
				[ ] - Useful
			[ ] - Train model for predictions
		[ ] - Show Tweets
			[ ] - Decision model
	[ ] - GUI
		[x] - Login Button
		[x] - Log Console
		[x] - CSV File Tree		
		[ ] - Filter tweets Dataframe
			[ ] - Filter by key and param
			[ ] - Filter by words included
			[ ] - Filter 
		[ ] - Display tweets / Dataframe
			[ ] - show comments quantity
			[ ] - show classification prediction
		[ ] - Manage CSV files
			[x] - Loading selected CSV
			[ ] - Save current DF to file
			[ ] - ReArange
				[ ] - Combine CSV  groups
					[ ] - By Lang
					[ ] - By User
					[ ] - Popular
					[ ] - Other features
			[ ] - Remove
				[ ] - Old
				[ ] - Used
				[ ] - Small
		