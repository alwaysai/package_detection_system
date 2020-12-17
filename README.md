# Package Detection System App
This app is designed to let you use your own custom package detection model to detect when packages arrive and when they are removed You'll need an alwaysAI account and to have alwayAI installed:

- [alwaysAI account](https://alwaysai.co/auth?register=true)
- [alwaysAI CLI tools](https://dashboard.alwaysai.co/docs/getting_started/development_computer_setup.html)

## Requirements
This app is intended to work on a model you've trained yourself! Follow the steps below before running your app. The alwaysAI support team is available on Discord to help you if you get stuck: https://discord.gg/rjDdRPT.

### Collect a Dataset
To get you up and running, we've prepared a [dataset](https://www.alwaysai.co/docs/_static/beta/Packages.zip) that includes a few hundred images of packages being placed and removed from an outdoor doorstep. This app will work best using a model that has been trained on your own doorstep (or wherever you intend to run your app), so we encourage you to add to this dataset. See [this doc](https://alwaysai.co/docs/model_training/data_collection.html#data-capture-guidelines) for data collection tips). For speedy data collection, you can use this [image capture app](https://github.com/alwaysai/expanded-image-capture-dashboard) available on the alwaysAI GitHub. Also checkout the [hacky hour](https://www.youtube.com/watch?v=jNpxVea8F9Q&feature=youtu.be) on the package dataset collection for tips on how to set up your own data collection process.

### Annotate your Data
Then you can annotate your data, using [this guide](https://alwaysai.co/docs/model_training/data_annotation.html).

### Train your Model
 Then, follow the [training section](https://alwaysai.co/docs/model_training/quickstart.html#step-3-train-your-model) of our quickstart guide to train your own model. You'll find links to tips for data collection and annotation on that page as well.  

### Set up your Project
Clone this repo into a local directory. Then cd into new folder and run `aai app configure` and make the following selections:
- When prompted to choose a project, use the down arrow and select `Create new project`, choosing any name you like.
- Choose to run either locally or on an edge device.

The `app.py` and `alwaysai.app.json` files should be automatically detected and you should not need to create them.

You can find details on working with projects [here](https://alwaysai.co/docs/getting_started/working_with_projects.html).

You can either publish your model and add it to your project using `aai app models add`, or test out an unpublished version using the `--local-version` flag with this command. See [this documentation](https://alwaysai.co/docs/model_training/using_your_model.html) for full details.

Finally, you'll need to replace the model that is used to create `package_detector` in `app.py` with the name of your own model! 

## Running

This app is set up to use a USB camera from a laptop. You can [change the media](https://alwaysai.co/docs/edgeiq_api/video_stream.html) input to whatever best suits your use case.

Run the project as you would any alwaysAI app! See [our docs pages](https://alwaysai.co/blog/building-and-deploying-apps-on-alwaysai) if you need help runnig your program.

#### Example Output

Engine: Engine.DNN
Accelerator: Accelerator.GPU

Model:
testuser/package_detector

Labels:
['???', 'package']

Engine: Engine.DNN
Accelerator: Accelerator.GPU

Model:
alwaysai/mobilenet_ssd

Labels:
['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

[INFO] Streamer started at http://localhost:5000
Wed Dec 16 17:09:05 2020: No person detected.
More packages have arrived!

Wed Dec 16 17:09:08 2020: No person detected.
More packages have arrived!

Wed Dec 16 17:09:12 2020: No person detected.
PACKAGES MAY HAVE BEEN REMOVED

## Troubleshooting
Docs: https://dashboard.alwaysai.co/docs/getting_started/introduction.html

Community Discord: https://discord.gg/rjDdRPT

Email: support@alwaysai.co