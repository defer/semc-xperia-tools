#!/usr/bin/env python
#
# Copyright 2012 Diogo Ferreira <defer@cyanogenmod.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import shutil
import os

EXPECTED_RPM_BIN_OFFSET = 0x494d84

def print_usage():
    print 'Usage: %s <input boot image> <rpm.bin> <output boot image> [expected hex offset]' % sys.argv[0]

def log(s):
    print '[xperia-rpm-patcher] %s' % s

def patch_rpm (boot_image, rpm_bin, output_file, rpm_offset):
    current_size = os.stat(boot_image).st_size
    rpm_size = os.stat(rpm_bin).st_size

    log ('Preflight check')

    if current_size > rpm_offset:
        log ('Please make sure the boot image has at most %d bytes' %
                rpm_offset)
        sys.exit(1)

    log ('Kanging boot image')
    # create a copy for patching
    shutil.copyfile(boot_image, output_file)

    # get the rpm contents
    rpm_input = open(rpm_bin,'r')
    rpm_content = rpm_input.read()

    log ('Adding tons of zeroes!')
    # open our output file
    boot_image_output = open(output_file, 'a+')

    # add zero-padding up until the rpm_offset
    for i in xrange(0, rpm_offset - current_size):
        boot_image_output.write(chr(0))

    log ('Adding the special sauce')
    # append the rpm contents
    for byte in rpm_content:
        boot_image_output.write(byte)

    # we're done
    boot_image_output.close()

    log ('Done. So long and thanks for all the fish.')


if __name__== '__main__':
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    boot_image = sys.argv[1]
    rpm_bin = sys.argv[2]
    output_file = sys.argv[3]
    rpm_offset = EXPECTED_RPM_BIN_OFFSET
    if len(sys.argv) == 5:
        rpm_offset = int(sys.argv[4],16)

    patch_rpm (boot_image, rpm_bin, output_file, rpm_offset)

