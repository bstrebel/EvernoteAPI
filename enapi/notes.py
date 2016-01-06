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
        self._tags = None
        self._index = 0
        self._offset = 0
        self.logger.debug('Notebook [%s] %s' % (self.guid, self.name.decode('utf-8')))

    @property
    def notes(self):
        if self._notes is None:
            self._notes = {}
            for nmd in self._client.note_store.findNotesMetadata(self._note_filter, 0, 2048, self._note_spec).notes:
                nmd = EnNote.initialize(nmd)
                self._notes[nmd.guid] = nmd
        return self._notes

    @property
    def tags(self):
        if self._tags is None:
            self._tags = {}
            for tag in self._client.note_store.listTagsByNotebook(self.guid):
                self._tags[tag.guid] = tag.name
        return self._tags

    @property
    def client(self):
        if self._client is None:
            self._client = EnClient.get_client()
        return self._client

    @property
    def logger(self): return self.client.logger

    def __getitem__(self, guid):
        return self.notes.get(guid)

    def __iter__(self):
        return iter(self.notes)

    def get_tag(self, guid):
        return self.tags.get(guid)

    def get_tag_by_name(self, name):
        for k,v in self.tags.items():
            if v == name:
                return k
        return None

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
        self._book = None
        self.__initialize()

    def __initialize(self):
        self._client = EnClient.get_client()
        self._book = None
        #self.logger.debug('Note [%s] %s' % (self.guid, self.title.decode('utf-8')))
        self.logger.debug('Note [%s] %s' % (self.guid, self.title))

    @property
    def client(self):
        if self._client is None:
            self._client = EnClient.get_client()
        return self._client

    @property
    def book(self):
        if self._book is None:
            self._book = self.client.notebook(self.notebookGuid)
        return self._book

    @property
    def logger(self): return self.client.logger

    @property
    def view_url(self):
        return "http://%s/shard/%s/nl/%s/%s/" % (self.client.service,
                                                 self.client.user.shardId,
                                                 self.client.user.id, self.guid)

    @property
    def edit_url(self):
        return "https://%s/Home.action#n=%s&b=%s&ses=4&sh=1&sds=5&" % (self.client.service, self.guid, self.notebookGuid)

    @property
    def plain(self):
        from enapi import PlainTextOfENML
        if self.content is not None:
            return PlainTextOfENML(self.content)

    @property
    def html(self):
        from enapi import HTMLOfENML
        # if self.content is not None:
        #     return HTMLOfENML(self.content)
        return self.content

    @property
    def categories(self):
        """
        :return: comma separated list of unicode tags
        """
        if self.tagGuids:
            return ','.join(map(lambda guid: self.book.get_tag(guid).decode('utf-8'), self.tagGuids))

    @property
    def tags(self):
        """
        :return: array of tag names
        """
        names = []

        if self.tagGuids:
            for guid in self.tagGuids:
                name = self.book.get_tag(guid)
                names.append(name)

        return names

    def html_content(self, url=None):
        if url:
            if self.attributes.sourceURL:
                if not self.attributes.sourceURL.startswith(url):
                    return True
        return False

    @property
    def encoded(self):
        if isinstance(self.title, unicode):
            self.title = self.title.encode('utf-8')

        if isinstance(self.content, unicode):
            self.content = self.content.encode('utf-8')
        return self

    def load(self, maxsize=None, resource=False, recognition=False, alternate=False):
        content = True
        if maxsize:
            if self.contentLength and self.contentLength > maxsize:
                content = False
                message = "Note content exceeds limit of %d KB" % (maxsize/1024)
        try:
            note = self.client.note_store.getNote(self.guid, content, resource, recognition, alternate)
            self = EnNote.initialize(note)
            if not content and not self.content:
                self.content = message
            return self
        except Exception, e:
            self.logger.exception(e)
            return None

    def delete(self):
        self.client.delete_note(self.guid)

    def create(self):
        return(EnNote.initialize(self.client.note_store.createNote(self.encoded)))

    def update(self):
        return(EnNote.initialize(self.client.note_store.updateNote(self.encoded)))

    def get_note(self, content=False, resource=False, recognition=False, alternate=False):
        return self.client.note_store.getNote(self.guid, content, resource, recognition, alternate)

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
