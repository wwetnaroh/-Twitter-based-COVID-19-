## Twitter-based COVID-19 Data Processing

### <li>COVID-19 Data Map</li>
A US state map reflects the COVID-19 severity in every state in different colors.

### <li>Real-time Twitter Popular Hashtags</li>
The hashtags related to COVID-19 post by users are collected and sorted by mentioned frequency. Due to the limitation of server performance, we select the top 20 most fre- quent hashtags and present them in a word- cloud format. The word size is proportional to the appearance frequency of the related hashtags on Twitter. And the word-cloud is updated every 30 seconds.

### <li>History Data Streaming</li>
Sometimes we want to track the history of the most popular hashtags records on Twit- ter instead of the real-time result. Thus, we implement the Twitter history function to insulate the popular hashtags records from May 16th to May 18th, 2020.

### <li>Sentimental Analysis on Real-time Tweets</li>
According to the pulled tweets from Twitter API, semantic analysis is carried out to classify them into three classes, including positive, negative, and neutral. The number of each class is represented in the pie chart.

## Demo video