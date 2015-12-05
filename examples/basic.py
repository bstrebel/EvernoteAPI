#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests

from enapi import EnClient

en = EnClient.get_client()
print en.user_store.getUser().name

for name in en.notebooks:
    print name

for nmd in en.notebook('Office'):
    #note = nmd.get_note()
    print(nmd.title)
    print(nmd.attributes)

#en._initialize()



