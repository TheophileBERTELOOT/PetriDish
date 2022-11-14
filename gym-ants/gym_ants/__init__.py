from gym.envs.registration import register

register(
    id='ants-v0',
    entry_point='gym_ants.envs:AntsEnv',
)