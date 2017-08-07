#!/usr/bin/env python3

import trunc


def test_version_number():
    package_version = trunc.__version__
    print("package version is {}".format(package_version))
    assert '0.0.1a1' == package_version
