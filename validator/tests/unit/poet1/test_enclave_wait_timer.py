# Copyright 2016 Intel Corporation
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
# ------------------------------------------------------------------------------

import unittest
import time

import pybitcointools

from journal.consensus.poet1.poet_enclave_simulator.enclave_wait_timer \
    import EnclaveWaitTimer


class TestEnclaveSimulatorWaitTimer(unittest.TestCase):

    @classmethod
    def _create_random_key(cls):
        return pybitcointools.random_key()

    def test_create_wait_timer(self):
        wait_timer = \
            EnclaveWaitTimer(
                duration=3.14159,
                previous_certificate_id='Bond.  James Bond.',
                local_mean=2.71828)

        self.assertAlmostEquals(wait_timer.duration, 3.14159, 3)
        self.assertLessEqual(wait_timer.request_time, time.time())
        self.assertEqual(
            wait_timer.previous_certificate_id, 'Bond.  James Bond.')
        self.assertAlmostEquals(wait_timer.local_mean, 2.71828, 3)
        self.assertIsNone(wait_timer.signature)

    def test_serialize_wait_timer(self):
        wait_timer = \
            EnclaveWaitTimer(
                duration=3.14159,
                previous_certificate_id='Bond.  James Bond.',
                local_mean=2.71828)

        self.assertIsNotNone(wait_timer.serialize())

    def test_deserialized_wait_timer(self):
        wait_timer = \
            EnclaveWaitTimer(
                duration=3.14159,
                previous_certificate_id='Bond.  James Bond.',
                local_mean=2.71828)

        serialized = wait_timer.serialize()
        signing_key = self._create_random_key()
        wait_timer.signature = \
            pybitcointools.ecdsa_sign(serialized, signing_key)

        copy_wait_timer = \
            EnclaveWaitTimer.wait_timer_from_serialized(
                serialized,
                wait_timer.signature)

        self.assertAlmostEquals(
            wait_timer.request_time,
            copy_wait_timer.request_time)
        self.assertAlmostEquals(
            wait_timer.duration,
            copy_wait_timer.duration)
        self.assertEqual(
            wait_timer.previous_certificate_id,
            copy_wait_timer.previous_certificate_id)
        self.assertAlmostEquals(
            wait_timer.local_mean,
            copy_wait_timer.local_mean)
        self.assertEqual(
            wait_timer.signature,
            copy_wait_timer.signature)

        self.assertEqual(serialized, copy_wait_timer.serialize())
