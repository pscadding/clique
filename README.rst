######
Clique
######

Manage collections with common numerical component.

.. code-block:: python

    >>> import os
    >>> import clique
    >>> collections, remainder = clique.assemble(os.listdir('.'))
    >>> for collection in collections:
    ...     print collection
    file.%04d.jpg [1-5, 8, 10-15]
    file.%04d.dpx [1-15]


*************
Documentation
*************

Full documentation can be found at http://clique.readthedocs.org

*************
Issue tracker
*************

Found a bug? Have an idea on how to make the tool better?

Post it at https://gitlab.com/4degrees/clique/issues

*********************
Copyright and license
*********************

Copyright (c) 2013 Martin Pengelly-Phillips

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License in the LICENSE.txt file, or at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

