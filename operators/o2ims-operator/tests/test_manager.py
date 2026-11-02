###########################################################################
# Copyright 2026 The Nephio Authors.
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
##########################################################################

import importlib
from pathlib import Path
import sys
from unittest import mock


CONTROLLERS_DIR = Path(__file__).parents[1] / "controllers"


def test_manager_starts_northbound_api(monkeypatch, tmp_path):
    token_file = tmp_path / "token"
    token_file.write_text("")
    monkeypatch.setenv("TOKEN", str(token_file))
    monkeypatch.syspath_prepend(str(CONTROLLERS_DIR))

    try:
        with mock.patch("threading.Thread") as thread:
            manager = importlib.import_module("manager")
    finally:
        sys.modules.pop("manager", None)

    thread.assert_called_once_with(target=manager.run_flask, daemon=True)
    thread.return_value.start.assert_called_once_with()
