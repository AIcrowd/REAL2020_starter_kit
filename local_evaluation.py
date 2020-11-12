import numpy as np
import real_robots
from my_controller import SubmittedPolicy
from interval import interval

#########################################################
### Please specify the action_type and n_objects here ###
###     These will be used during your evaluation     ###
#########################################################
EVALUATION_ACTION_TYPE = 'joints'
EVALUATION_N_OBJECTS = 1
DATASET_PATH = "./data/goals-REAL2020-s2020-25-15-10-%s.npy.npz" % EVALUATION_N_OBJECTS

result, detailed_scores = real_robots.evaluate(
                SubmittedPolicy,
                environment='R2',
                action_type=EVALUATION_ACTION_TYPE,
                n_objects=EVALUATION_N_OBJECTS,
                intrinsic_timesteps=15e6,
                extrinsic_timesteps=10e3,
                extrinsic_trials=50,
                visualize=False,
                goals_dataset_path=DATASET_PATH
                , video = (True, True, True)
            )

print(result)
print(detailed_scores)

result_data = {'result': result,
               'detailed_scores': detailed_scores}

run_id = np.random.randint(0, 1000000)

np.save("./R{}-{:.3f}".format(run_id, result['score_total']), result_data)
