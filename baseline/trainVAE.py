from baseline.abstractor import VAEAbstractor
from baseline.abstractor import currentAbstraction
import numpy as np
import baseline.config as config
import baseline.priorityQueue as pq
import cv2


if __name__ == "__main__":
    allActions = np.load(config.sim['experience_data'], allow_pickle=True).tolist()

    allAbstractedActions = [[currentAbstraction(a[0]), a[1],
                             currentAbstraction(a[2])]
                            for a in allActions]

    images = [action[2] for action in allAbstractedActions]
    print("Total images {} for VAE and BS".format(len(images)))
    cbsm = cv2.createBackgroundSubtractorMOG2(len(images))
    for i in range(len(images)):
        cbsm.apply(images[i])
    background = cbsm.getBackgroundImage()
    images = np.average(abs(images - background), axis=3) != 0
    ab = VAEAbstractor(images, latent_dim=7 * config.abst['n_obj'], retrain=True)

