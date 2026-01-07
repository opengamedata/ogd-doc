# Train Tab

In the train tab, you build machine learning pipelines (preprocessing and modeling) and perform model comparison.

All the values of the form **are saved** when sent to server after you hit **Train** button, and are restored when clicked on the model button in the **left side panel** in the **Models Bar View**.

## Model (hyper)parameters

**Target labels**: Use if you want to **exclude** segments with certain **labels** when training the model.

**Ratio of training data**: instead of using 80/20 train-test split, you can modify the proportion in case your full dataset is bigger or smaller.

**Class weights**: in cases when number of objects within **one category is much more than in other categories**, to avoid model bias to improve scores on one label, it's suggested to use class weights, so that errors in any class are penalized equally.

Another hyperparameter is the **model type**, which are explained in the next subsections

### Logistic Regression
The simplest and fastest model, can be useful as a baseline

**Regularization**: used to **reduce overfitting** (good train performance, poor test performance), increasing this parameter's value.

**Penalty**: type of the penalization, L1 or L2.

### Random Forest

Slightly more complex model, doesn't need scaling and null handling.

**Number of Estimators**: number of trees that will be used to generate the prediction, used to reduce overfitting.

**Max Depth**: increase to reduce bias.

### Neural Network
Most complex models, needs more time to train, but can discover complex patterns in the data.

**Epochs**: number of training epochs, increase to improve accuracy.

**Learning rate**: very low can lead to very slow learning, very high can lead to not converging to the optima.

**Hidden layers**: setting the shape of the neural network with ReLU activation.

## Dimensionality reduction
More complex model can lead to overfitting or multicolinearity. We need some techniques to reduce the size.

### Scaling
To keep the data ranges similar and avoid giving more importance to one variable because the range is bigger, you can use scaling. Usually, **Standard Scaling** will work out well.
### PCA
A common technique to reduce dimensions in high-dimensional data.

You can **visualize the plot** and select the number of components when the variance explained changed the most abrupt way. 

**Standar Scaling** is useful to make the plot look more smooth.

**If set to 0, PCA is disabled.**

### Features Selection
Selection of features can be performed manually (by default all the ogd features are excluded). 

The columns are colored using the **maximum Pearson correlation coefficients** with the **included features**. The greener is the selection, the less collinearity, means less duplicate information which is bad for the model.

The **Autoselect** button build a logistic regression with all features included and uses L1 penalization to exclude features with coefficient = 0, therefore performing and automatic features selection.
## Model comparison
We have a more visual **Bar View** and the classic **Table View** for model comparison.

The **left panel** is used for model selection to restore the parameters on the page. The **percentage** is the Test Accuracy.

The **center panel** has the plot of all the models' metrics, that can be changed using the **top dropdown** to use **label-specific metrics** (Precision, Recall) or **label-aggregated metrics**(Test and Train Accuracy, F1, AUC).

The **right panel** has the model summary, that has a confusion matrix, row count, columns count and the time performance.
## Applying models
**Apply Selected Model** is used to apply the last trained model or the currently selected in the models sidebar.

**Apply Best Model** is used to apply the best model by **test accuracy**.