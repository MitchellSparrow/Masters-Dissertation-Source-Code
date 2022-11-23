# LSTM Model

The following folder contains all of the code used to build and train the LSTM model.

# Training results

Training and validation classification accuracy vs epoch for the LSTM RNN:

![alt text](https://i.imgur.com/iufeQEO.png)

Training and validation loss vs epoch for the LSTM RNN. A log scale is used due to the large range in values:

![alt text](https://i.imgur.com/ndlotRH.png)

# Prediction Results

Stacked LSTM test set performance statistics including precision, recall, F1 score and classification accuracy:

![alt text](https://i.imgur.com/qoz7B2W.png)

From the above table, it can be seen that the precision, recall and F1 score are all on average above 90 %. Precision is the proportion of positive identifications which were actually correct and is calculated by dividing the true positives by all the positives. Recall on the other hand is the proportion of actual positives that was identified correctly and is a measure of the model correctly identifying true positives.

The F1 score combines both precision and recall into a single value that represents the harmonic mean of the two values. For more information on these metrics as well as the method in which they are calculated, please refer to section B.6 in the Appendix.

The no object, firm and very firm classes all had perfect precision, recall and F1 scores. The soft and medium classes on the other hand did not perform as well. The soft class had a precision of 0.75, and the medium class had a recall of 0.8. These are however respectable values given the small amount of data which was available.
