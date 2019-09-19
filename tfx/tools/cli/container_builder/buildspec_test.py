# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Tests for tfx.tools.cli.builder.buildspec."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os
import tensorflow as tf
import yaml

from tfx.tools.cli.builder import buildspec
from tfx.tools.cli.builder import commons


class BuildSpecTest(tf.test.TestCase):

  def _sort_dict(self, data):
    res = collections.OrderedDict()
    for k, v in sorted(data.items()):
      if isinstance(v, dict):
        res[k] = self._sort_dict(v)
      else:
        res[k] = v
    return res

  def test_generate_clean(self):
    test_buildspec_name = 'test_buildspec'
    default_buildspec_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'testdata',
        test_buildspec_name)
    buildspec.BuildSpec(
        filename=commons.BUILD_SPEC_FILENAME,
        target_image='gcr.io/test:dev',
        dockerfile_name=commons.DOCKERFILE_NAME)
    with open(default_buildspec_path, 'r') as f:
      golden_buildspec = yaml.safe_load(f)
    with open(buildspec.get_filename(), 'r') as f:
      generated_buildspec = yaml.safe_load(f)

    self.assertEqual(
        self._sort_dict(generated_buildspec), self._sort_dict(golden_buildspec))

    # clean up
    os.remove(buildspec.get_filename())

if __name__ == '__main__':
  tf.test.main()
