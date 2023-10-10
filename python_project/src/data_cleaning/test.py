import sys

sys.path.insert(0, "src/visualisation")
from eda import Eda

sys.path.insert(0, "src/sentiment_analysis")
from sa import Sentiment_analysis

sa = Sentiment_analysis()
vaders = sa.vader_polarity()
sa.polarity_score_by_rating(vaders)

eda = Eda()
eda.count_by_rating()
