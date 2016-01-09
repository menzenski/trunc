# -*- coding: utf-8 -*-

def to_unicode_or_bust(obj, encoding='utf-8'):
    """Return ``obj`` as ``unicode``.

    Credit for this function belongs to
    `Kumar McMillan <http://farmdev.com/talks/unicode>`.

    :param obj: the object to be returned as ``unicode``
    :type obj: ``str``, ``unicode``
    :param encoding: the desired encoding (UTF-8 is the default)
    :rtype: ``unicode``
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


