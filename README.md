# lerobot_robot_limx

LeRobot plugin for [LimX Dynamics](https://www.limxdynamics.com/) robots. One package, four
robot types — install it next to an unmodified LeRobot and the robots work with every
`lerobot-*` command.

| `--robot.type` | Robot | Joints | Notes |
|---|---|---|---|
| `limx_humanoid` | Oli (`HU_D04`) | 31 | Full-size humanoid: 2×6-DoF legs, 3-DoF waist, 2-DoF head, 2×7-DoF arms |
| `limx_luna` | Luna (`HU_L04`) | 27 | 2×6-DoF legs, 3-DoF waist, 2-DoF head, 2×5-DoF arms; ankles and waist driven through parallel linkages |
| `limx_tron1` | TRON1 | 6 / 8 | Point-foot (6), sole-foot (8) and wheel-foot (8) builds, selected by `ROBOT_TYPE` |
| `limx_tron2` | TRON2 | 16 + 2 | Dual-arm configuration: 16 servo joints plus a pair of grippers |

All four command joint positions in radians.

## Install

```bash
pip install lerobot_robot_limx
```

Nothing else is needed. LeRobot imports any installed package whose name starts with
`lerobot_robot_` when it starts, and this package registers the four types above with its
config system. No patching, no plugin list to edit, no fork of LeRobot.

The vendor SDKs (`limxsdk`, and `tron2-env` for TRON2) are dependencies of this package and are
installed automatically on Linux and Windows. They ship no macOS wheels, so on macOS the drivers
install but cannot connect.

Requirements: Python 3.12+, LeRobot 0.4+.

## Without a robot: check that the install worked

You do not need hardware to confirm the plugin is wired up correctly.

```bash
python -c "import lerobot_robot_limx; print(lerobot_robot_limx.__version__)"
lerobot-record --robot.type=limx_humanoid --help
```

What you should see:

- the version prints (e.g. `0.1.0`)
- `--help` runs and lists `limx_humanoid` options — this proves the type registered

Connecting without a robot will time out with an error mentioning the configured address. That is
the expected failure and it means everything up to the network connection is working.

To run the test suite locally:

```bash
pip install 'lerobot_robot_limx[dev]'
pytest -q
```

The driver tests run against stand-ins for the vendor SDKs, so they need no robot, no network and
no SDK installation.

## With a robot

Every robot is reached over IP; there is no separate driver installation step.

```bash
# Oli, at its default address
lerobot-record \
    --robot.type=limx_humanoid \
    --robot.robot_ip=10.192.1.2 \
    --robot.id=my-oli \
    --dataset.repo_id=${HF_USER}/oli-test \
    --dataset.num_episodes=2 \
    --dataset.single_task="wave"
```

TRON1 additionally needs the build selected, because the joint table depends on it:

```bash
export ROBOT_TYPE=PF_TRON1A    # or SF_TRON1A / WF_TRON1A
lerobot-record --robot.type=limx_tron1 --robot.robot_ip=10.192.1.2 ...
```

TRON2 uses LimX's public runtime and expects a `port` on the robot's on-board bridge:

```bash
lerobot-record --robot.type=limx_tron2 --robot.robot_ip=10.192.1.2 --robot.port=8000 ...
```

### Simulator

`limxsdk` reaches a simulator the same way it reaches a robot — point `robot_ip` at
`127.0.0.1` and start the matching MuJoCo simulator:

| Robot | Simulator |
|---|---|
| TRON1 | [tron1-mujoco-sim](https://github.com/limxdynamics/tron1-mujoco-sim) |
| TRON2 | [tron2_mujoco_sim](https://github.com/limxdynamics/tron2_mujoco_sim) |
| Oli | [humanoid-mujoco-sim](https://github.com/limxdynamics/humanoid-mujoco-sim) |

This is how the drivers were exercised against the real SDK without hardware.

### Robot models

URDF, MJCF and USD files live in their own repositories rather than in this package: the meshes
alone are far larger than the driver, and simulators load them from disk.

| Robot | Models |
|---|---|
| Oli | [humanoid-description](https://github.com/limxdynamics/humanoid-description) |
| Luna | [luna-description](https://github.com/limxdynamics/luna-description) |
| TRON1 | [tron1-robot-description](https://github.com/limxdynamics/tron1-robot-description) |
| TRON2 | [tron2-robot-description](https://github.com/limxdynamics/tron2-robot-description) |

This package ships the drivers only. Nothing in it needs those files to talk to a robot.

## Known limitations

- **No cameras.** These drivers expose joint positions only, so a recorded dataset is
  proprioceptive. The vendor stacks carry the image path; wiring it in here is planned and does
  not need an upstream review.
- **Oli and Luna have not been run on physical hardware.** Joint order, names, gains and control
  mode come from LimX's published controllers, but the standing behaviour is unconfirmed on a real
  machine. TRON1 and TRON2 have been exercised against the vendor SDK.
- **Luna has no default gains.** `kp`/`kd` are required in the config, because the only published
  Luna gains belong to its motion-tracking policies and are defined in motor space for the parallel
  linkages, which makes them unusable as joint-space defaults.
- **`robot_type` is not validated by the vendor package on Oli and Luna**, so a wrong value selects
  the wrong joint table silently. Set it deliberately.

## Maintained by LimX Dynamics

This package is maintained by the vendor, not by an outside contributor. Bug reports and hardware
questions go to the [issue tracker](https://github.com/limxdynamics/lerobot_robot_limx/issues);
changes that need `limxsdk` behaviour we do not control are raised with the SDK team directly.

## License

Apache-2.0.
