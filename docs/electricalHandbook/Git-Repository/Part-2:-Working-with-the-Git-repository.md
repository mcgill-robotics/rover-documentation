---
title: Part 2: Working with the Git repository 
---

**Working with the Git repository** 

Before you read this make sure you know at least a bit about how git works. You can read the Git Basics section of this handbook for that.

This section of the handbook will help you with contributing your change to our git repository while keeping things clean and organized.

**Where do I put my code?**  
   
There are folders for each subsystem on the rover in the repo. Find the subsystem your task is part of and create a folder inside the subsystem’s folder. (Make sure to keep reading, there’s a section of this document for how to make your folder) 

One exception to this would be Python scripts and libraries we create for software to use. Those should go under the bridge/src folder.

**Other than my code, should I add any other files?**

Yes\! Try to add a README.md to your project’s folder. The README should contain the following things:

* Your project’s name as a title  
* The link to your documentation on the documentation website if it's ready  
* A short description of what it does  
* If applicable some short instructions for how to use it  
* Any other things you feel would be useful to someone looking at your project’s folder.

**What should I name my files/folder?**

For project folders, prefer using a snake case convention (file\_name\_like\_this). Inside your project you may name things however you like if it makes your work easier. 

For files, you can name them however you like (except for python files in the bridge folder, this must be in snake case to allow import in Python)

**I made some changes on my computer. How do I send them to GitHub?**

* Stage your files with git add  
* Make sure you're on the right branch  
* Make a commit with git commit  
* Then push your changes with git push

PS: Make sure you read the rest of this document before doing anything, it answers some questions you may have about committingz branching and pushing.

**Should I push to the main branch?**

No\! The main branch should be as bug-free as possible so we should never push directly to it. All changes should be in their own branch where they can be checked before being merged to main.

**How do I name my branch?**

Prefer naming branches by first adding one of the following prefixes: 

* feat/ if your task adds new firmware/features  
* fix/ if you are fixing a bug in existing firmware,   
* docs/ if you are updating READMEs or doing other documentation tasks  
* chore/ if you're moving things around for organization.

Then add a descriptive name for the changes you're going to make, this will typically be a short name that describes your task. This description should be in kebab-case (project-name-like-this) and all lowercase.

*Example branch name:*   
feat/arm-can-integration

**What do I write in my commit messages?**

Describe the changes you made in the commit. Try to mention what project it affects and what new features of bug fixes you made. An example of a good commit message would be:  
pantilt: added control for both servos with pwm

**I’m done with my task now what?**

Once you're done with a task open a pull request on GitHub. With the pull request, the leads will merge your code into the main branch. This way we can keep all the complete code organized neatly under the main branch. 

**Any other tips and tricks?**

* Commit and push frequently\!  
  Making small commits for each of your changes, makes it easier to revert bad changes if something goes wrong and to see what you have changed compared to a mega commit. Pushing often helps others collaborate with you because they will more often have the latest version of your code.  
* Make short-lived branches  
  Try to keep branches focused on small changes by breaking down your task. If your firmware is brand new and you're starting multiple things at the same time, it’s ok to have a longer living task but once you're done you should open a pull request and merge it to main. If you find bugs after that, that’s ok just open a new branch for the bugfix and the close it once that's also fixed.  
* Talk to your taskmates (and other elec members)  
  Make sure you communicate with others so people know what you're working on. That helps prevent conflicts from multiple people working on the same thing (and you get to know each other better)

🥳 Now you're ready to start adding code to our repo. For more advanced use cases, there is another document in the handbook with more rules and guidelines. If you need to know those, your leads will inform you, otherwise go have fun with your task\!