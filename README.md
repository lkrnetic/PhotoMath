# PhotoMath

In order to run this project you should have installed Git and download and install Git Large File Storage: https://git-lfs.github.com/

Also, Anaconda should be installed in order to run Python notebooks. 

Once you make folder where are other Anaconda Python noteebooks, you should run  ```git lfs install```

Then you should run ```git clone https://github.com/lkrnetic77/PhotoMath```

After that make Python virtual environment https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

Then run ```pip install numpy opencv-python imutils tensorflow==2.3.1```

### About Android app and back end
I made Android app that capture photo and send to captured photo to backend, but unfortunately I couldn't install Tensorflow on Heroku because installing Tensorflow on Heroku exceed limits - I couldn't find any other free server.

### About improving accuracy and metrics
In order to increase accuracy, it would be good to train longer, use more data augmentation, track data about data (metadata) and see with regards to what metadata model fails to give prediction. Also, it would be good to do cross validation and construct confusion matrix too see if there exists reletionship so that when model fails to predict X, model usually predict Y. In that case, it would be good to check if data is properly labeled and increase amount of photos of class X.
