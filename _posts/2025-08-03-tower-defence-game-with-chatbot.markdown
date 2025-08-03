---
layout: post
title: "Experiment: Making a TD game with just a free chatbot and zero game dev skills"
date:   2025-08-03 12:00:09 +0200
categories: posts
permalink: /:collection/:title
---

# The beginning

![logo.png](/assets/images/8/logo.png){:style="float: left; width:20%; margin-right: 30px; margin-bottom: 30px"}
TL;DR: I had an idea to create a small game within a few hours, despite having no previous experience in game development, no fancy tools, and relying on a free chatbot to guide me on that journey. It didn't work as expected. However, it became an enjoyable experience that I want to share with you.

(Note: The character icons and the welcome screen image were generated with assistance from AI.)

To see the final result, please click [here.](/td-v-0-0-1)

<div style="clear:both;"></div>

# Preparation

Nowadays, numerous discussions, myths, and confusion surround the use of AI to replace developers. Therefore, I decided to conduct a small experiment that was supposed to take a few hours. The idea was quite simple: to create a tiny tower defence game.


Firstly, I defined the project's vision and requirements. The initial project goal was described as follows.

- It should be a classical tower defence game, where the goal for the player is to build towers that can shoot enemies and prevent them from reaching the target.
- Each tower requires a certain amount of money to build. It can gather experience and eventually get some upgrades. Towers have other parameters, such as health, ammo, and range.
- Enemies should be spawned in waves, increasing the complexity with every next one.
- There should be two different types of enemies. One attacks from a distance; once it has no ammo, it should switch to a melee attack. Second has only a melee attack mode.
- Enemies should try to reach the center of the map. Once a tower is encountered on the way, they should stop and attack it.
- A map is represented as a grid of a particular size and has a "base" in the center that is the ultimate goal for the enemies.
- The "base" has health points. Once an enemy has reached it, it should take some damage. Finally, when the "base's" health level is 0, the game is over.
- The player gains gold by killing enemies.
- The towers gain experience while shooting enemies.
- The game should have an isometric view.

Secondly, I have established some additional constraints and requirements for the project.

- The game should be implemented in pure JavaScript, without relying on any external libraries.
- It should be playable in the browser without an internet connection.
- There should be a build pipeline that allows me to produce a single artifact(HTML page) that can be distributed. Therefore, all components, such as code and images, must be embedded.
- The game source code should be obfuscated.
- I must mention that JavaScript was chosen, not only because it can be executed in the browser, but also because I am not an expert in it. I've let the chatbot make all the decisions regarding the code design and implementation.

At that point, I was ready to start with a game.

# The first try

After waiting for a while, I have got the first version of the code. Even without being an expert in JS, I have realized that what I have got is a horror. Needless to say, it didn't work, but the approach that was taken seemed to be wrong. Everything was built around DOM manipulation, standalone functions, and event listeners that were scattered throughout the code. When I tried to run it, before it crashed, some random colored squares were flying around at the speed of light. That was fun, but painful to watch.

# Try again

I raised my complaints to the chatbot, claiming that I am not entirely happy with the result and asked to "fix everything", emphasizing that the game doesn't look isometric, it crashes, and in general, it is so broken, so I have a hard time even describing what is exactly wrong about it.

Surprisingly, the next version of the generated code was way better. The chatbot created classes for each type of entity in the game and provided me with a list of helper methods to work with the grid. After that, with the following few prompts, where I have described how the towers and enemies should look and behave, I have received something that wasn't crashing anymore.

I was indeed inspired by the progress we had made and was willing to move forward; however, I was suddenly informed that my free chat quota had already been used, and I would need to wait to continue.

I have tried to continue with completely free models, but it was like talking to a stranger. Answers were disconnected from the context, and in general, the quality was significantly lower.

# And again

At that point, I had already answered my initial question: writing my game with a free version of the chatbot within a few hours was impossible, at least due to the quota limits. However, I was already enjoying the process and decided to continue. Therefore, after a short break, I have continued.

At this time, the code was already quite extensive; for this reason, I have split it into separate files, each responsible for a different aspect of the game. It has reduced the amount of data I had to share with the bot every time.

Every time I asked, for example, to change the behavior of the bullets, I had to provide the necessary information about the grid or actors' implementations, and so on. Sometimes, without these hints, answers drifted away from reality, and as a consequence, I had to edit the code manually or even start a new chat.

# And again

Time was passing, and the codebase was growing; some bugs were fixed, while others were added.

There were some good moments, such as when the chatbot added animation and logic to the artillery shell based on my very vague prompt. At the same time, I have spent a few hours arguing with it regarding how the actors should be positioned on the grid.

Anyway, step by step, the game was getting closer to what I had initially intended.

# First results

A few days later, I was trying to play what we had done. It was a satisfying feeling because the game was working. Here, I am referring only to the technical definition of "working", which in this case means crashing rarely rather than every time.

![first_result.png](/assets/images/8/first_result.png)

The lack of game design experience became very apparent at this stage.

Some of the major problems were related to the UI:

- Game elements were not "interactive". For example, there was no animation when the mouse was over a tower.
- Selection of some elements on the field was not possible because they were hidden behind each other.
- Some elements improperly overlapped during the rendering.
- There was no welcome screen, and at least some images for the tower type selection dialog.
- The UI was overwhelmed with unnecessary information, such as reload time and ammo level bars, that was not relevant to the game process.

Some significant problems with the gameplay:

- Some game mechanics, such as the ammo limit for the tower, didn't fit at all because it is reset with each new level, and the level-up occurs before the tower runs out of ammo.
- Difficulty was absolutely out of control. The initial game configuration proposed by the chatbot made the game too hard and too fast.
- There was no pause in the game, and combining it with UI issues, it was not possible to control the towers on time.

Nevertheless, the main issue was technical. The game experienced a significant performance issue, with extremely low FPS.

At this moment, I had decided to call the initial experiment done and to take a closer look at the code.

As I said earlier, JavaScript is not the language I know well and am aware of its best practices; however, it was obvious that the code has, at least, an "average" quality. Things that I have recognized immediately were:

- Code duplication and improper encapsulation. For example, logic specific to the shooting by different tower types was implemented in both the Bullet and Tower classes.
- No optimizations, such as caches, are used for repetitive operations like distance calculations.
- Same event listeners were defined multiple times.

After I mentioned some particular places to the chatbot, it was able to improve the overall performance, but I have no idea how much of the code base is still done suboptimally.

# Final steps

During the last iteration, I have tried to address the most problematic issues.

- I have updated the appearance of the towers and removed unnecessary information adjacent to them to minimize visual clutter and prevent game elements from overlapping.
- The chatbot-generated images were used for the welcome window and for selecting the type of tower.
- I attempted to adjust the game's difficulty manually, but I believe it has compromised the game's balance in the final version.
- Some code optimization was introduced to the code with the help of a chatbot. However, overall performance is still poor; I can tell this from the noise of my laptop's fan.
- The pause button was added, and this changed the gameplay entirely. The game became way easier and less competitive.

The final step was to add the Makefile to build the export version of the HTML page. Needless to say, these types of tasks are handled just perfectly by the chatbot. Within just a few rounds of prompts, I have achieved what I wanted.

<video controls="controls">
  <source src="/assets/video/8/demo.mp4" type="video/mp4">
</video>

# Conclusion

Working on that project was indeed fun. However, returning to the initial goals, I have mixed feelings about the outcome. On the one hand, I have obtained the first results very quickly using a chatbot, and it shone when I had to generate images or write a Makefile.

However, there are two significant concerns from my side, regarding the generated code, assuming that I am not deeply familiar with JavaScript:

1. The generated code didn't represent best practices and, in general, had arguable quality. Therefore, its use for the production or educational purposes is questionable. Additionally, the manual interaction was required at some stage anyway.
2. Another open question is the time I have spent relying on the chatbot. Of course, if I were to use the paid version with higher quotas, it could be way efficient (and expensive). However, considering this particular project with the mentioned constraints and efforts I have spent trying to explain problems in the chat, perhaps it would be faster to learn some JS and write it from scratch.

Additionally, the chatbot didn't prevent me from making poor game design decisions; moreover, it contributed to some of them. It makes me to believe that human expertise remains necessary and that domain experts are valuable, just as they have always been.

Putting it all together, even if my experiment has failed, I think that using chatbots gives an advantage these days. Of course, hallucinations, privacy, and security concerns are present; however, I believe that the biggest disappointment stems from wrong expectations about them. They are great tools that have a significant impact on the industry, and unthinkingly neglecting or ignoring them seems to me too conservative and even risky in the long run.