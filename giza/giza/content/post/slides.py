# Copyright 2014 MongoDB, Inc.
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

import os
import logging

from giza.tools.command import command
from giza.content.post.archives import slides_tarball, get_tarball_name

logger = logging.getLogger('giza.content.post.slides')

def slides_output(conf):
    cmd = 'rsync --recursive --times --delete {src} {dst}'

    dst = os.path.join(conf.paths.public_site_output, 'slides')

    if not os.path.exists(dst):
        logger.debug('created directories for {0}'.format(dst))
        os.makedirs(dst)

    builder = 'slides'

    if 'edition' in conf.project and conf.project.edition != conf.project.name:
        builder += '-' + conf.project.edition

    command(cmd.format(src=os.path.join(conf.paths.branch_output, builder) + '/',
                       dst=dst))

    logger.info('deployed slides local staging.')

def slide_tasks(sconf, conf, app):
    task = app.add('task')
    task.job = slides_tarball
    task.target = [get_tarball_name('slides', conf),
                   get_tarball_name('link-slides', conf)]
    task.args = [sconf.name, conf]
    task.description = "creating tarball for slides"

    task = app.add('task')
    task.job = slides_output
    task.args = [conf]
    task.description = 'migrating slide output to production'
