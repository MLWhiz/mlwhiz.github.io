
# Adding Interpretability to Multiclass Text Classification models

Adding Interpretability to Multiclass Text Classification models

### ELI5: Add explainability but not at a loss to accuracy

Explain Like I am 5.

It is one of the basic tenets of learning for me where I try to distill any concept in a more palatable form. As Feynman said:
> # I couldn’t do it. I couldn’t reduce it to the freshman level. That means we don’t really understand it.

So, when I saw the ELI5 library that aims to interpret machine learning models, I just had to try it out.

One of the basic problems we face while explaining our complex machine learning classifiers to the business is ***interpretability***.

Sometimes the stakeholders want to understand — what is causing a particular result? ***It may be because the task at hand is very critical and we cannot afford to take a wrong decision. ***Think of a classifier that takes automated monetary actions based on user reviews.

***Or it may be to understand a little bit more about the business/the problem space.***

Or it may be to increase the ***social acceptance ***of your model.

***This post is about interpreting complex text classification models.***

## The Dataset:

To explain how ELI5 works, I will be working with the stack overflow dataset on Kaggle. This dataset contains around 40000 posts and the corresponding tag for the post.

This is how the dataset looks:

![](/images/interpret/0.png)

And given below is the distribution for different categories.

![](/images/interpret/1.png)

This is a balanced dataset and thus suited well for our purpose of understanding.

So let us start. You can follow along with the code in this [Kaggle Kernel](https://www.kaggle.com/mlwhiz/interpreting-text-classification-models-with-eli5)

## Staring Simple:

![[Interpretable ML Book](https://christophm.github.io/interpretable-ml-book/terminology.html)](/images/interpret/2.png)*[Interpretable ML Book](https://christophm.github.io/interpretable-ml-book/terminology.html)*

Let us first try to use a simple scikit-learn pipeline to build our text classifier which we will try to interpret later.*** In this pipeline, I will be using a very simple count vectorizer along with Logistic regression.***

    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.pipeline import make_pipeline

    # Creating train-test Split
    X = sodata[['post']]
    y = sodata[['tags']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # fitting the classifier
    vec = CountVectorizer()
    clf = LogisticRegressionCV()
    pipe = make_pipeline(vec, clf)
    pipe.fit(X_train.post, y_train.tags)

Let’s see the results we get:

    from sklearn import metrics

    def print_report(pipe):
        y_actuals = y_test['tags']
        y_preds = pipe.predict(X_test['post'])
        report = metrics.classification_report(y_actuals, y_preds)
        print(report)
        print("accuracy: {:0.3f}".format(metrics.accuracy_score(y_actuals, y_preds)))

    print_report(pipe)

![](/images/interpret/3.png)

The above is a pretty simple Logistic regression model and it performs pretty well. ***We can check out its weights using the below function:***

    for i, tag in enumerate(clf.classes_):
        coefficients = clf.coef_[i]
        weights = list(zip(vec.get_feature_names(),coefficients))
        print('Tag:',tag)
        print('Most Positive Coefficients:')
        print(sorted(weights,key=lambda x: -x[1])[:10])
        print('Most Negative Coefficients:')
        print(sorted(weights,key=lambda x: x[1])[:10])
        print("--------------------------------------")

    ------------------------------------------------------------
    OUTPUT:
    ------------------------------------------------------------

    Tag: python
    Most Positive Coefficients:
    [('python', 6.314761719932758), ('def', 2.288467823831321), ('import', 1.4032539284357077), ('dict', 1.1915110448370732), ('ordered', 1.1558015932799253), ('print', 1.1219958415166653), ('tuples', 1.053837204818975), ('elif', 0.9642251085198578), ('typeerror', 0.9595246314353266), ('tuple', 0.881802590839166)]
    Most Negative Coefficients:
    [('java', -1.8496383139251245), ('php', -1.4335540858871623), ('javascript', -1.3374796382615586), ('net', -1.2542682749949605), ('printf', -1.2014123042575882), ('objective', -1.1635960146614717), ('void', -1.1433460304246827), ('var', -1.059642972412936), ('end', -1.0498078813349798), ('public', -1.0134828865993966)]
    --------------------------------------
    Tag: ruby-on-rails
    Most Positive Coefficients:
    [('rails', 6.364037640161158), ('ror', 1.804826792986176), ('activerecord', 1.6892552000017307), ('ruby', 1.41428459023012), ('erb', 1.3927336940889532), ('end', 1.3650227017877463), ('rb', 1.2280121863441906), ('gem', 1.1988196865523322), ('render', 1.1035255831838242), ('model', 1.0813278895692746)]
    Most Negative Coefficients:
    [('net', -1.5818801311532575), ('php', -1.3483618692617583), ('python', -1.201167422237274), ('mysql', -1.187479885113293), ('objective', -1.1727511956332588), ('sql', -1.1418573958542007), ('messageform', -1.0551060751109618), ('asp', -1.0342831159678236), ('ios', -1.0319120624686084), ('iphone', -0.9400116321217807)]
    --------------------------------------
    .......

And that is all pretty good. We can see the coefficients make sense and we can try to improve our model using this information.

But above was a lot of code. ***ELI5 makes this exercise pretty simple for us***. We just have to use the below command:

    import eli5
    eli5.show_weights(clf, vec=vec, top=20)

![](/images/interpret/4.png)

Now as you can see the weights value for Python is the same as from the values we got from the function we wrote manually. And it is much prettier and wholesome to explore.

But that is just the tip of the iceberg. ELI5 can also help us to debug our models as we can see below.

## Understanding our Simple Text Classification Model

Let us now try to find out why a particular example is misclassified. I am using an example which was originally from the class Python but got misclassified as Java:

    y_preds = pipe.predict(sodata['post'])

    sodata['predicted_label'] = y_preds

    misclassified_examples = sodata[(sodata['tags']!=sodata['predicted_label'])&(sodata['tags']=='python')&(sodata['predicted_label']=='java')]

    ***eli5.show_prediction(clf, misclassified_examples['post'].values[1], vec=vec)***

![](/images/interpret/5.png)

![](/images/interpret/6.png)

In the above example, the classifier predicts Java with a low probability. And we can examine a lot of things going on in the above example to improve our model. For example:

1. We get to see that the classifier is taking a lot of digits into consideration(not good)which brings us to the conclusion of cleaning up the digits. Or replacing DateTime objects with a DateTime token.

1. Also see that while dictionary has a negative weight for Java, the word dictionaries has a positive weight. So maybe stemming could also help.

1. We also see that there are words like <pre><code> that are influencing our classifier. These words should be removed while cleaning.

1. Why is the word date influencing the results? Something to think about.

We can take a look at more examples to get more such ideas. You get the gist.

## Going Deep And Complex

This is all good and fine but*** what if models that we use don’t provide weights for the individual features like LSTM?*** It is with these models that explainability can play a very important role.

![](/images/interpret/7.png)

To understand how to do this, we first create a TextCNN model on our data. *Not showing the model creation process in the interest of preserving space* but think of it as a series of preprocessing steps and then creating the deep learning model. If interested, you can check out the modelling steps in this [Kaggle kernel](https://www.kaggle.com/mlwhiz/interpreting-text-classification-models-with-eli5).

***Things get interesting from our point of view when we have a trained black-box model object.***

ELI5 provides us with theeli5.lime.TextExplainer to debug our prediction - to check what was important in the document to make a prediction decision.

To use [**TextExplainer](https://eli5.readthedocs.io/en/latest/autodocs/lime.html#eli5.lime.lime.TextExplainer)** instance, we pass a document to explain and a black-box classifier (a predict function which returns probabilities) to the [**fit()](https://eli5.readthedocs.io/en/latest/autodocs/lime.html#eli5.lime.lime.TextExplainer.fit)** method. From the documentation this is how our predict function should look like:
> **predict** (*callable*) — Black-box classification pipeline. ***predict*** should be a function which takes a list of strings (documents) and return a matrix of shape ***(n_samples, n_classes)*** with probability values - a row per document and a column per output label.

So to use ELI5 we will need to define our own function which takes as input a list of strings (documents) and return a matrix of shape ***(n_samples, n_classes).** You can see how we first preprocess and then predict.*

    def predict_complex(docs):
        # preprocess the docs as required by our model
        val_X = tokenizer.texts_to_sequences(docs)
        val_X = pad_sequences(val_X, maxlen=maxlen)
        y_preds = model.predict([val_X], batch_size=1024, verbose=0)
        return y_preds

Given below is how we can use TextExplainer. Using the same misclassified example as before in our simple classifier.

    import eli5
    **from eli5.lime import TextExplainer**

    **te = TextExplainer(random_state=2019)**
    te.fit(sodata['post'].values[0], predict_complex)
    te.show_prediction(target_names=list(encoder.classes_))

![](/images/interpret/8.png)

This time it doesn’t get misclassified. You can see that the presence of keywords dict and list is what is influencing the decision of our classifier. One can try to see more examples to find more insights.

***So how does this work exactly?***

[**TextExplainer](https://eli5.readthedocs.io/en/latest/autodocs/lime.html#eli5.lime.lime.TextExplainer)** generates a lot of texts similar to the document by removing some of the words, and then trains a white-box classifier which predicts the output of the black-box classifier and not the true labels. The explanation we see is for this white-box classifier.

This is, in essence, a little bit similar to the Teacher-Student model distillation, where we use a simpler model to predict outputs from a much more complex teacher model.

Put simply, it tries to create a simpler model that emulates a complex model and then shows us the simpler model weights.

## Conclusion
> # Understanding is crucial. Being able to interpret our models can help us to understand our models better and in turn, explain them better.

ELI5 provides us with a good way to do this. It works for a variety of models and the [documentation](https://eli5.readthedocs.io/en/latest/index.html) for this library is one of the best I have ever seen.

Also, I love the decorated output the ELI5 library provides with the simple and fast way it provides to interpret my models. And debug them too.

To use ELI5 with your models you can follow along with the code in this [Kaggle Kernel](https://www.kaggle.com/mlwhiz/interpreting-text-classification-models-with-eli5)

## Continue Learning

If you want to [learn](https://towardsdatascience.com/how-did-i-start-with-data-science-3f4de6b501b0?source=---------8------------------) more about NLP and how to create Text Classification models, I would like to call out the [***Natural Language Processing](https://www.coursera.org/learn/language-processing?ranMID=40328&ranEAID=lVarvwc5BD0&ranSiteID=lVarvwc5BD0-HcQgnbxBjnlE7bTEy2jJRw&siteID=lVarvwc5BD0-HcQgnbxBjnlE7bTEy2jJRw&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0)*** course in the [**Advanced machine learning specialization](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0)**. Do check it out. It talks about a lot of beginners to advanced level topics in NLP. You might also like to take a look at some of my [posts on NLP](https://towardsdatascience.com/tagged/nlp-learning-series) in the NLP Learning series.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources as sharing knowledge is never a bad idea.
