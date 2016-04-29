==================================================================
Describing user by his Instagram page using machine learning
==================================================================

### Description of repo
- env_data.py (Set of functions for getting labels and features from MongoDB)
- plot_data.py (Few functions for plotting, using matplotlib)
- Haruspex_sex_prediction.ipynb (Jupyter notebook with predictions for user's sex, using 5 main algorithms)
- Haruspex_age_prediction.ipynb (The same, but for user's age)
- dump/users (1351 users, will be much more soon)

### Installation
```bash
git clone https://github.com/pavlovdog/haruspex.git
cd haruspex
mongorestore --db users dump/users
```

### Algorithmes:
- SVM
- Decision trees
- Naive Bayes
- Logistic regression
- K-nearest neighbours

### Labels
- Age (+)
- Sex (+)
- Interests
- Attitude to alcohol
- Attitude to smoking
- Current relationships

### Features
- Number of followers (+)
- Number of followings (+)
- Number of media (+)
- Average number of likes (+)
- Average number of comments (+)
- Average number of medias per week (+)
- Average number of mentions
- Average number of tags
- List of tags
- List of followings
- Average number of smileys in caption (+)
- Average caption's length (+)
- Correlation between videos & photos (+)
- Frequency of new medias (+)
- List of filteres
