# Survey study on factors moderating lifestyle and eating habits

The aim of the study was to find out if there were differences between Americans and Italians in eating habits, and which variables could explain them better.

The subjects were selected from social groups and a Reddit post.

### Cleaning

The missing values and issues with my survey software were handled in the file **Cleaner.ipynb**, where I also create the target variable 'diet health score', that is how good is the diet of the subject based on their self-reported weekly eating habits.

### Analysis

I did univariate and multivariate exploratory analysis in the file EDA.ipynb, exploiting the most interesting variables

### Models

I created 3 models: 

- A Linear Regression Model trained to predict 'diet health score' given every other parameter but the ones used to generate the first, that achieved 'only' an R squared score of 0.33, but it gave us a lot of insights on the data through the coefficients of the parameters, for example we learned that skipping meals was correlated with a bad diet health score, and that people who cooked usually had higher diet health score

- A Logistic Regression Model, trained to predict if the subject was Italian or American. It achieved an accuracy score of almost **93%**, and an R squared of more than **68%**.  
Again the coefficients were really useful, showing us that American subjects are less likely to practice a sport, but when they do, they commit harder than Italians. Also Americans eat 'less health' proteic foods, like meat and eggs, while Italians eat more 'good' proteins like legumes and fish.

- Then I've built a cluster model, with K-means algorithm, that had the same objective of the Logistic Model, but performed worst, with only 61% of accuracy.

### Conclusions

I believe that the survey was able to exploit the differences in eating habits between the different populations, and to give us ideas and proofs of what could mediate those differences.