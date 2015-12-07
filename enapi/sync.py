#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json, re, requests
from pysync import Sync
from enapi import *


class EnClientSync(Sync):

    def __init__(self, client, options):

        self._name = options.get('notebook')
        self._guid = options.get('guid')
        self._key_attribute = options.get('key')
        self._book = None

        if isinstance(client, EnClient):
            self._client = client
        else:
            self._client = EnClient.get_client(**client)

    @property
    def client(self): return self._client

    @property
    def guid(self): return self._guid

    @property
    def name(self): return self._name

    def sync_map(self):
        # from enapi import EnBook
        if self.guid:
            self._book = EnBook.initialize(self._client.note_store.getNotebook(self.guid))
            self._name = self._book.name
        else:
            self._book = self._client.notebook(self._name)
            self._guid = self._book.guid

        self._items = {}
        for key in self._book:
            nmd = self._book.get_note(key)
            self._add_item(nmd.guid, nmd.updated, eval('nmd.' + self._key_attribute))
        return {'items': self.items, 'name': self.name, 'id': self.guid}

    def get(self):
        #note = self._client.note_store.getNote(guid, True, True, True, True)
        #nmd = self._client.get_note(self._key, self._name)
        nmd = self._book.get_note(self._key)
        return nmd

    def delete(self, this):
        self._client.delete_note(self._key)

    def create(self, this, that):
        pass

    def update(self, this, that):
        pass

