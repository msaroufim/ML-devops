# How to setup many ML experiments at scale

ML is a highly empirical discipline so the more experiments you can launch, the faster you can learn. This isn't a complex topic by typical Dev Ops standard but it's something I've noticed many ML people don't try to get better at. This repo shows a config driven experimentation workflow that'll help you launch tons of experiments and come back at night to check out what worked and what didn't.

## High level idea

1. Read a config either from CLI or YAML file
2. Print at the arguments you're using for an experiment and in your ML code make sure to log data either via tensorboard or manual print statements
4. Run lots of experiments at once then come back end of day to see what worked

## CLI vs YAML

CLI is actually the simplest method sine you just need to then create a shell script where you put all the commands you'd like to run

If you'd like more fine grained control you can use ```yamlparser.py``` but then in your code need to make sure you handle the arguments yourself

## Print arguments

Before every training run print all the relevant argumetns in your experiment at the very top. This way you can identify the run you're on.

Below those print statements make sure to also print your training loss, accuracy and other relevant details like ```model.summary()``` 

Make sure tensorboard callbacks are activated so you can inspect all your charts


## Run lots of experiments at once

This is as simple as running ```sample_runner.sh``` but because this script may be really long running, it's possible you can disconnect from it and will have to restart your work.

To avoid these problems make sure to run ```nohup sample_runner.sh &```

Now you can freely close your laptop if you're working with some remote host like AWS

To inspect your results you can use ```tail -f nohup.out``` to inspect it live, otherwise just open ```nohup.out``` with your favorite text editor

Note that the scripts will run sequentially and for the most part that is OK since you want to use the full resources of any machine you're on. If you're interested in more distributed work there are frameworks that help you do this.

## Notification
I don't like constantly checking whether my experiments or done so I make sure to add the below to the end of any long running script so I get an email notification when everything is done. You can even pass ```nohup.out``` directly in the email body to get everything without having to log back into the server.

```sudo apt install mailutils```
```mail -s 'message subject' username@gmail.com <<< 'testing message body' ```
