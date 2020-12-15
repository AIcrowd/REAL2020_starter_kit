# Baseline 

## Context description
Before describing the system, let's bring back to memory the competition context in which it operates:

There is an Agent-Environment context in which the agent has control of a robotic arm and the environment includes a table and a cube, in addition to the robotic arm. The agent must learn to use the robotic arm in such a way as to be able to move the cube at any point on the table without any prior knowledge. The agent will therefore have to collect different skills and, on request, be able to use them to move the object from one position to another.

![Extrinsic phase](https://github.com/emilio-cartoni/REAL2020_starter_kit/blob/master/baseline/media/extrinsic_phase_little_video.gif)

## Approach to the problem
The problem was addressed with several components: Policy, Explorer, Abstractor and Planner. We will expose the system with a top-down approach, then we will first see the Policy component and lastly the Plan.

![Architecture](https://github.com/emilio-cartoni/REAL2020_starter_kit/blob/master/baseline/media/architecture.svg)

### Policy component
The Policy component represents the agent and defines its behavior depending on the phase in which it is located. In the intrinsic phase it will deal with exploring (using explorer) the space of actions [1] in order to collect as many actions as possible. In the extrinsic phase he will deal with using the collected actions to generate sequences (using planner and abstractor) of actions that lead to the desired state [2].

[1]: with action is meant a triple (precondition, trajectory, postcondition)

[2]: with state is meant a cube (x,y) position

![Policy flow](https://github.com/emilio-cartoni/REAL2020_starter_kit/blob/master/baseline/media/class_policy.svg)

### Explorer component
The Explorer component deals with the exploration of the two-dimensional space above the table. To do this it generates one points in the four-dimensional space (x1, y1, x2, y2) which then the Policy component uses to create a trajectory on the table. Before making the movement corresponding to the trajectory, the agent saves the current state of the world so that the triple (precondition, trajectory, postcondition) can be saved later, where postcondition is the state of the world after performing the action . This exploration phase corresponds to the intrinsic phase, where the agent limits himself to collecting actions to perform at his best in the extrinsic phase.

### Abstractor component
The abstractor is the component that modify the actions elements to ensure that the planning work. This is done in dynamic way: it use a Variational Auto-Encoder (VAE) to extrapolate a latent space on which it can work. After that it takes the actions collected in the intrinsic phase and for each state variable extrapolates the most significant distances. In other words, for each variable we have a set of points and these points have a distance between them. Each distance will have a certain frequency and therefore a relevance, we are interested in the latter. To derive the most relevant distances, the abstractor calculates all the distances between precondition and postcondition. These will represent all the distances experienced as an effect of actions, after which it sorts these distances and samples them equally distributed according to the number of abstractions required by the config file (it contain all hyperparameters value). These differences will allow the agent to discretize the state space and to distinguish on the basis of the current abstraction between actions that modify the state of the world and actions that do not.

### Planner component
The Planner component has an instance of the abstraction tool available which will allow it to access the distance associated with each level of abstraction. The planner uses the abstractor to make ever more abstract plans until he finds a plane, where "more and more abstract" means more collapse between states. Before moving on to planning, it prepare the actions in the following way: calculate the distance between each precondition and postcondition and if this is smaller than the distance associated with the current abstraction, then the action in question is ignored. The abstraction is done incrementally from the bottom up until a plane is found. This will ensure that it prefer plans with lower abstraction.

## Config file
The agent's behavior also depends on hyperparameters specified in the config.yaml file. These parameters are divided into 3 different categories: abstraction, planner and simulation. Below we explain their semantics:
 - Abstraction:
   - precision: allows to truncate the numbers contained in the vector representing the state of the world to the i-th digit after the comma.
   - n_obj: allow to specify how many objects is present in the simulation
   - type: with the possible values ​​[pos, pos_noq, image, filtered_mask] allows you to specify if you want to use the position of the objects with quaternion, position of the objects without quaternion, world situation image and world situation mask respectively.
   - total_abstraction: allows you to specify how many equally distributed samples you want to take in the set of differences experienced between precondition and postcondition
   - percentage_of_actions_ignored_at_the_extremes: allows you to specify the percentage that you want to ignore at the extremes of the actions (sorted). This variable was made in such a way as to be able to eliminate the most unlikely actions to be performed.
 - Planner:
   - replan: allows you to specify if you want the agent to replan after each action performed
   - try_random: allows you to specify if you want the agent to do random actions if he does not find a plan
   - type: with the possible values ​​[mega, noplan] it allows to specify if you want to plan, or not
   - action_size: allows you to specify the length of the actions that the planner takes into consideration in order to give an upper limit to the sequence of actions to be planned
 - Simulation:
   - experience_data: allows you to specify the file to be used to face the extrinsic phase
   - extrinsic_steps: the length of an extrinsic trial (10.000 timesteps) 
   - save_images: allows you to specify if you want the actions to contain in preconditions and postconditions the state image rather than just the coordinates of the cube.
   - save_masks: allows you to specify if you want the actions to contain in preconditions and postconditions the state mask, where a mask is a image that specify what object is content in each image pixel, rather than just the coordinates of the cube.
   - use_experience_data: allows you to specify if you want to use the file specified in "experience_data", or (if false) if you want to use the actions collected in the intrinsic phase just carried out

# Experience data
At the end of a simulation, the baseline will save all the actions experienced during the intrinsic phase in an .npy file.
This npy file contains several numpy.ndarray consisting of three elements: 
- pre condition: it is a triple containing the image, the coordinates and the mask which represented the world state before execute the action.  
- action: it is the action executed to get the post condition
- post condition: it is a triple containing the image, the coordinates and the mask which represented the world state after execute the action.  
If save_images or save_masks are set to false in the config file, the corrisponding elements in the pre and post conditions will have no value.

**Attention -** Saving images and masks can lead to very large files (up to 7.6 GB for 15M timesteps intrinsic phase with both images and masks).

Examples of an .npy file for a full 15M timestep intrinsic phase can be downloaded from the following links:
- macro_action with only the cube object: [google drive link](https://drive.google.com/file/d/1Sf9bSYftixq732ZijzNvHh6UA6OMyYlt/view?usp=sharing)
- macro_action with the cube and tomato objects: [google drive link](https://drive.google.com/file/d/1AZuAQQr2IE6JU2SoCMS0PO69o1wQ1c_L/view?usp=sharing)
- joint with only the cube object: [google drive link](https://drive.google.com/file/d/12j-RzgnnGDDsuWO58uAcaM_h_2xj9cxE/view?usp=sharing)

These can also be downloaded with wget command:
- macro_action with only the cube object:  
`wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Sf9bSYftixq732ZijzNvHh6UA6OMyYlt' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Sf9bSYftixq732ZijzNvHh6UA6OMyYlt" -O transitions_file.zip && rm -rf /tmp/cookies.txt`
- macro_action with the cube and tomato objects:  
`wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AZuAQQr2IE6JU2SoCMS0PO69o1wQ1c_L' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AZuAQQr2IE6JU2SoCMS0PO69o1wQ1c_L" -O double_objects.zip && rm -rf /tmp/cookies.txt`
- joint with the cube object:  
`wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=12j-RzgnnGDDsuWO58uAcaM_h_2xj9cxE' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=12j-RzgnnGDDsuWO58uAcaM_h_2xj9cxE" -O joints_transitions_file.zip && rm -rf /tmp/cookies.txt`

**Attention -** Before the files can be used you need to extract in the data folder (contained in the main folder) the npy file from the zip file.
