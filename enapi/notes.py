#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
from enapi import *

class EnBook(Types.Notebook):

    @staticmethod
    def initialize(nb):
        nb.__class__ = EnBook
        nb.__initialize()
        return nb

    def __init__(self, **kwargs):
        Types.Notebook.__init__(self, **kwargs)
        self._notes = None
        self._client = None
        self.__initialize()

    def __initialize(self):
        self._client = EnClient.get_client()
        self._note_filter = NoteStore.NoteFilter(notebookGuid=self.guid)
        self._note_spec = NoteStore.NotesMetadataResultSpec(includeTitle=True,
                                                            includeContentLength=True,
                                                            includeCreated=True,
                                                            includeUpdated=True,
                                                            includeDeleted=True,
                                                            includeTagGuids=True,
                                                            includeAttributes=True)
        self._notes = None
        self._index = 0
        self._offset = 0

    @property
    def notes(self):
        if self._notes is None:
            self._notes = {}
            for nmd in self._client.note_store.findNotesMetadata(self._note_filter, 0, 2048, self._note_spec).notes:
                nmd = EnNote.initialize(nmd)
                self._notes[nmd.guid] = nmd
        return self._notes

    @property
    def client(self):
        if self._client is None:
            self._client = EnClient.get_client()
        return self._client

    def __getitem__(self, guid):
        return self.notes.get(guid)

    def __iter__(self):
        return iter(self.notes)

    def get_note(self, guid):
        return self.notes.get(guid)

    def create_note(self, note):
        note.notebookGuid = self.guid
        return self.client.create_note(note)

    def update_note(self, note):
        note.notebookGuid = self.guid
        return self.client.update_note(note)

    def delete_note(self, guid):
        return self.client.delete_note(guid)

class EnNote(Types.Note):

    @staticmethod
    def body(body):

        div = ""
        for line in body.splitlines():
            div += "<div>" + line + "</div>"

        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        xml += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
        xml += "<en-note>%s</en-note>" % div
        return xml

    @staticmethod
    def initialize(nmd):
        nmd.__class__ = EnNote
        nmd.__initialize()
        return nmd

    def __init__(self, **kwargs):
        Types.Note.__init__(self, **kwargs)
        self._client = None
        self.__initialize()

    def __initialize(self):
        self._client = EnClient.get_client()

    @property
    def client(self):
        if self._client is None:
            self._client = EnClient.get_client()
        return self._client

    @property
    def view_url(self):
        return "http://%s/shard/%s/nl/%s/%s/" % (self.client.service,
                                                 self.client.user.shardId,
                                                 self.client.user.id, self.guid)

    @property
    def edit_url(self):
        return "https://%s/Home.action#n=%s" % (self.client.service, self.guid)

    @property
    def plain(self):
        from enapi import PlainTextOfENML
        if self.content is not None:
            return PlainTextOfENML(self.content)

    @property
    def html(self):
        from enapi import HTMLOfENML
        if self.content is not None:
            return HTMLOfENML(self.content)

    def load(self):
        note = self.client.note_store.getNote(self.guid, True, True, True, True)
        self = EnNote.initialize(note)
        return self

    def delete(self):
        self.client.delete_note(self.guid)

    def create(self):
        return(EnNote.initialize(self.client.note_store.createNote(self)))

    def get_note(self):
        return self.client.note_store.getNote(self.guid, True, True, True, True)

    # def __getitem__(self, key):
    #     # return note attributes
    #     pass
    #
    # def __getattr__(self, key):
    #     # return note attributes
    #     pass

class EnStack():

    def __init__(self):
        pass

    def __iter__(self):
        # return notebooks
        pass
