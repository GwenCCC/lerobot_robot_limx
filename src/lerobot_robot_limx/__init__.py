#!/usr/bin/env python

# Copyright 2025 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""LeRobot plugin for LimX Dynamics robots.

Installing this distribution is all a user has to do: LeRobot discovers any installed
package whose name starts with ``lerobot_robot_``, imports it on startup, and the four
robot types below register themselves with the config system.  Importing this module is
what performs that registration, so it must keep importing every subpackage eagerly.
"""

from .limx_humanoid import LimxHumanoid, LimxHumanoidConfig
from .limx_luna import LimxLuna, LimxLunaConfig
from .limx_tron1 import LimxTron1, LimxTron1Config
from .limx_tron2 import LimxTron2, LimxTron2Config

__version__ = "0.1.0"

__all__ = [
    "LimxHumanoid",
    "LimxHumanoidConfig",
    "LimxLuna",
    "LimxLunaConfig",
    "LimxTron1",
    "LimxTron1Config",
    "LimxTron2",
    "LimxTron2Config",
    "__version__",
]
