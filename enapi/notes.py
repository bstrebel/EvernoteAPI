#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types


class EnBook(Types.Notebook):

    @staticmethod
    def initialize(nb):
        nb.__class__ = EnBook
        nb._initialize()
        return nb

    def __init__(self):
        pass

    def _initialize(self):

        from enapi import EnClient
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

        # self._notes = self._client.note_store.findNotesMetadata(self._note_filter, 0, 10, self._note_spec)
        # for nmd in noteStore.findNotesMetadata(noteFilter, 0, 10, noteSpec).notes:
        # note = noteStore.getNote(nmd.guid, True, False, False, False)

    def _init_notes(self):
        if self._notes is None:
            # self._notes = []
            self._notes = {}
            for nmd in self._client.note_store.findNotesMetadata(self._note_filter, 0, 2048, self._note_spec).notes:
                nmd = EnNote.initialize(nmd)
                # self._notes.append(nmd)
                self._notes[nmd.guid] = nmd

    def get_note(self, guid):
        self._init_notes()
        return self._notes.get(guid)

    def __iter__(self):
        self._init_notes()
        return iter(self._notes)


class EnNote(Types.Note):

    @staticmethod
    def initialize(nmd):
        nmd.__class__ = EnNote
        nmd._initialize()
        return nmd

    def __init__(self):
        pass

    def _initialize(self):
        from enapi import EnClient
        self._client = EnClient.get_client()

    def get_note(self):
        return self._client.note_store.getNote(self.guid, True, True, True, True)

    def __getitem__(self, key):
        # return note attributes
        pass

    def __getattr__(self, key):
        # return note attributes
        pass

class EnStack():

    def __init__(self):
        pass

    def __iter__(self):
        # return notebooks
        pass
