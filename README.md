# How to setup many ML experiments at scale

ML is a highly empirical discipline so the more experiments you can launch, the faster you can learn. This isn't a complex topic by typical Dev Ops standard but it's something I've noticed many ML people don't try to get better at. This repo shows a config driven experimentation workflow that'll help you launch tons of experiments and come back at night to check out what worked and what didn't.

## High level idea

1. Read a config either from CLI or YAML file
2. Print at the arguments you're using for an experiment and in your ML code make sure to log data either via tensorboard or manual print statements
4. Run lots of experiments at once then come back end of day to see what worked

### Favorite tools
VS Code, tmate, hydra, weights and biases, docker, gradio, github actions and git-lfs - video covering all of these tools [here](https://www.youtube.com/watch?v=jmd-U-myaQY)

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

You can also run ```grep``` for some relevant lines in nohup in case you don't want to run the whole thing and customize your input with more useful ```print``` statements

Feel free to use Twilio or any notification from your favorite service

## Delayed start
If you want your script to start in 10 min then you can just run

```sleep 600 && script.sh```

For more complex time scheduling check out the ```at``` or ```batch``` utility

It's also useful to log the time your script started so just add the ```date``` command in between each command

## Retrain a model everytime you load new data
Use a cronjob

```crontab -e```

For example, run every minute ```* * * * script.sh```

Customize schedule https://phoenixnap.com/kb/set-up-cron-job-linux

## Tmux or screen to keep track of various sessions
Think of this as nohup on steroids, cheat sheet here https://tmuxcheatsheet.com/


## Git LFS

Use Git LFS to keep track of both your checkpoints and code in case your machine gets lost or you get locked out of it

## Monitor Machine and Processes

```htop``` is amazing - you can use to sort all processes in a tree like fashion, kill them instead of getting the process id via something like ```ps aux | grep processname```. See per core CPU and memory utilization

## SSH port forwarding
If you'd like to see a Jupyter notebook running on remote on your local machine 

1. remoteuser@remotehost: jupyter notebook --no-browser --port=XXXX
2. localuser@localhost: ssh -N -f -L localhost:YYYY:localhost:XXXX remoteuser@remotehost
3. In your browser: localhost:YYYY

Also works great for Tensorboard

# Fast deployment and profiling 
(Pytorch only)
1. deploy using Flask and ngrok
2. Trace with torch.fx https://pytorch.org/tutorials/intermediate/fx_profiling_tutorial.html
3. Use trace to profile with chrome://tracing

https://colab.research.google.com/drive/1t0fnm1GMpYkrGH9UDizIv2lo2_JlZ6sU?usp=sharing

# Reproducible work

Both Machine Learning and really any scientific endeavor face a reproducibility crisis. The best references on this topic are [Richard McElreath talk](https://www.youtube.com/watch?v=zwRdO9_GGhY&ab_channel=RichardMcElreath) for science and [Denny Britz blogpost]() for machine learning.

So reproducibility has a few aspects
1. Reproducible code - solved with ``` git log --pretty=format:'%h' -n 1```
2. Reproducible data - solved with ```SQL + AWS```
3. Reproducible runs - solved with ```logging tips from above section```
4. Reproducible environments - solved with ```pip, pytest and circleci```

Thankfully there are simple solutions for 1, 2, 3 - namely git.

If your code and data are version controlled and you create logs for your run which you also version control then ``` git log --pretty=format:'%h' -n 1``` will solve most of your problems.

So I want to talk more about reproducible environments 4

## Reproducible environments
Reproducible environments also has a few subproblems but the main goal is to make sure if you run your code from last week or if your collaborator wants to run your code then your results would remain consistent.

First step is to create a virtual environment for your project

```python3 -m venv yourvenv```

While developing you're going to be ```pip install ...``` a bunch of stuff

Once you're done make sure to run

```pip freeze > requirements.txt``` to keep track of the all dependencies your project has. Trust me this will save you a lot of time and heartache.

Tests in python are simple to setup

```pip install pytest pytest-cov```

```python
# in file test_library.py
import your_library

class TestLibrary:
    def test_function(self):
        assert expected_result = your_library.your_library_function(input1)
```

```pytest -v --cov```

This will solve 99% of your reproducibility problems, once your code needs to make it in production you can look into continuous integration by building your code in a docker container and automatically checking if your code passes.

## Passwords suck
```sh
ssh-keygen -t rsa
eval `ssh-agent`
ssh-add .ssh/id_rsa
ssh-copy-id -i .ssh/id_rsa.pub remoteuser@remoteserver
ssh -vvv -i .ssh/id_rsa remoteuser@remoteserver
```

## VSCode instead of VIM
With VS code you can SSH into into a remote server and mount it locally so you can use the same dev environment locally as you do remotely

In particular the Python debugger is pretty great when you want to set breakpoints and inspect the values of objects

Cmd Shift P and select the Python interpreter you want then go to ```launch.json``` and create a new launch config for your script where 

Setup up a program with the link to the file you want to start in and then you can pass in all the args you need as an array

Example here https://twitter.com/marksaroufim/status/1298044117973233665

![image](https://user-images.githubusercontent.com/3282513/110737305-fdc36d80-81e1-11eb-969b-dd9b708baca8.png)


## Favorite linux utilities
* Xarg lets shell commands accept input from stdin - 1? ```Echo {one two three} | xargs mkdir```
* Sort and cut also useful
* ```1>&2``` is a trick to redirect stdout to stderr - print both to console and file
```Htop | Awk ‘{print $1}’``` prints the 1 column - very practical 
printenv 
* ```Cnrl-x Cnrtl-e``` to start editing command in CLI in vim 
* Run a command until it succeeds ```while true do ping google.com 2>&1 && break done;```
* Record command line session: ```script```
* ```Cd -``` 
* ```Pushd and popd``` to save and pop directories
* ```Df -h``` to get file size in human readable format
* ```Diff``` command between 2 files
* History then !line_number to run that command without retyping
* Tmux cheat sheet https://tmuxcheatsheet.com/ 
    * Tmux ls 
    * Tmux attach -t session
    * Cntrl b q to switch panes
    * Cntrl b %, “ to split panes
* ```Rsync``` is a private owned dropbox
* Yes command ```yes | sudo apt-get install package``` in case you're brave and want to step away from your machine

