#!/usr/bin/env python

############################################################################
# 
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
# 
#  This file is part of the example classes of the Qt Toolkit.
# 
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
# 
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
# 
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
############################################################################

import sys
import random
from PySide import QtCore


DataSize = 100000
BufferSize = 8192
buffer = range(BufferSize)

bufferNotEmpty = QtCore.QWaitCondition()
bufferNotFull = QtCore.QWaitCondition()
mutex = QtCore.QMutex()
numUsedBytes = 0


class Producer(QtCore.QThread):
    def run(self):
        global numUsedBytes

        for i in range(DataSize):
            mutex.lock()
            if numUsedBytes == BufferSize:
                bufferNotFull.wait(mutex)
            mutex.unlock()
            
            buffer[i % BufferSize] = "ACGT"[random.randint(0, 3)]

            mutex.lock()
            numUsedBytes += 1
            bufferNotEmpty.wakeAll()
            mutex.unlock()


class Consumer(QtCore.QThread):
    def run(self):
        global numUsedBytes

        for i in range(DataSize):
            mutex.lock()
            if numUsedBytes == 0:
                bufferNotEmpty.wait(mutex)
            mutex.unlock()
            
            sys.stderr.write(buffer[i % BufferSize])

            mutex.lock()
            numUsedBytes -= 1
            bufferNotFull.wakeAll()
            mutex.unlock()
            
        sys.stderr.write("\n")


if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)
    producer = Producer()
    consumer = Consumer()
    producer.start()
    consumer.start()
    producer.wait()
    consumer.wait()
