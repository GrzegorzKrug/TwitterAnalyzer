from Analyzer.Analyzer import Analyzer

app = Analyzer()
for x in range(10):  # 10 x 60min 
    app.collect_new_tweets(n=60, chunk_size=200, interval=60)
input('Press key....')
