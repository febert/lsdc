""" Hyperparameters for Large Scale Data Collection (LSDC) """
from __future__ import division

from datetime import datetime
import os.path

import numpy as np

from lsdc import __file__ as gps_filepath
from lsdc.agent.mjc.agent_mjc import AgentMuJoCo

from lsdc.gui.config import generate_experiment_info

from lsdc.proto.gps_pb2 import JOINT_ANGLES, JOINT_VELOCITIES, \
        END_EFFECTOR_POINTS, END_EFFECTOR_POINT_VELOCITIES, ACTION, \
        RGB_IMAGE, RGB_IMAGE_SIZE

IMAGE_WIDTH = 80
IMAGE_HEIGHT = 60
IMAGE_CHANNELS = 3

num_objects = 3

SENSOR_DIMS = {
    JOINT_ANGLES: 2+ 7*num_objects,  #adding 7 dof for position and orentation for every free object
     JOINT_VELOCITIES: 2+ 6*num_objects,  #adding 6 dof for speed and angular vel for every free object; 2 + 6 = 8
    #JOINT_ANGLES: 5,
    #JOINT_VELOCITIES: 5,
    END_EFFECTOR_POINTS: 3,
    END_EFFECTOR_POINT_VELOCITIES: 3,
    ACTION: 2,
    RGB_IMAGE: IMAGE_WIDTH*IMAGE_HEIGHT*IMAGE_CHANNELS,
    RGB_IMAGE_SIZE: 3,
}

BASE_DIR = '/'.join(str.split(gps_filepath, '/')[:-2])
EXP_DIR = BASE_DIR + '/../experiments/lsdc_exp/'


common = {
    'experiment_name': 'my_experiment' + '_' + \
            datetime.strftime(datetime.now(), '%m-%d-%y_%H-%M'),
    'experiment_dir': EXP_DIR,
    'data_files_dir': EXP_DIR + 'data_files/',
    'target_filename': EXP_DIR + 'target.npz',
    'log_filename': EXP_DIR + 'log.txt',
    'conditions': 1,
    'no_sample_logging': True,
}

if not os.path.exists(common['data_files_dir']):
    os.makedirs(common['data_files_dir'])

agent = {
    'type': AgentMuJoCo,
    'filename': './mjc_models/pushing2d.xml',
    'x0': np.array([0., 0., 0., 0.]),
    'inital_object_pos': np.array([0.3, 0., 0., 1., 0., 0., 0.,     # in global coordinates
                                   -0.3, 0., 0., 0, 1, 0., 0.,
                                   0.2, 0.3, 0., 0, 1, 0., 0.,]),

    # 'x0': [np.array([0., 0., 0., 0.]), np.array([0., 1., 0., 0.])],
    'dt': 0.05,
    'substeps': 6,
    'conditions': common['conditions'],
    'T': 500,
    'sensor_dims': SENSOR_DIMS,
    'state_include': [JOINT_ANGLES, JOINT_VELOCITIES, END_EFFECTOR_POINTS, END_EFFECTOR_POINT_VELOCITIES],
    'obs_include': [JOINT_ANGLES, JOINT_VELOCITIES, END_EFFECTOR_POINTS, END_EFFECTOR_POINT_VELOCITIES, RGB_IMAGE],
    'camera_pos': np.array([0., 0., 0., 3.90, -45., 90.]),
    'joint_angles': SENSOR_DIMS[JOINT_ANGLES],  #adding 7 dof for position and orentation of free object
    'joint_velocities': SENSOR_DIMS[JOINT_VELOCITIES],
}


config = {
    'num_samples': 1,
    'verbose_trials': 1,
    'verbose_policy_trials': 1,
    'common': common,
    'agent': agent,
    'gui_on': False,
}

# common['info'] = generate_experiment_info(config)