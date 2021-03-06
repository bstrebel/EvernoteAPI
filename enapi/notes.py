#!/usr/bin/env python
# -*- coding: utf-8 -*-

from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
from enapi import *
from pyutils import utf8, string

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
        self.logger.debug(u'Notebook [%s] %s' % (self.guid, utf8(self.name)))

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
        note = self.notes.get(guid)
        note._book = self
        return note

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
        self._properties = None
        self._tags = None
        self.logger.debug(u'Note [%s] %s' % (self.guid, utf8(self.title)))

    def properties(self):
        if self._properties is None:
            self._properties = []
            for k,v in self.__class__.__dict__.iteritems():
                if isinstance(v, property):
                    self._properties.append(k)
        return self._properties

    def __getitem__(self, key):
        if key in self.__dict__:
            # index[] based access non-property values
            return self.__dict__.get(key)
        # index[] based access to @property
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key in self.properties():
            # works only if @key.setter is defined !!!
            setattr(self, key, value)
        else:
            # non-property attributes
            self.__dict__[key] = value

    # def __getattr__(self, key):
    #     # return note attributes
    #     pass

    # @property
    # def title(self):
    #     return self.__dict__['title'].decode('utf-8')
    #
    # @title.setter
    # def title(self, value):
    #     self.__dict__['title'] = value

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
        return "https://%s/shard/%s/nl/%s/%s/" % (self.client.service,
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
            return ','.join(map(lambda guid: utf8(self.book.get_tag(guid)), self.tagGuids))
        else:
            return ''

    @property
    def tags(self):
        """
        :return: array of tag names
        """
        names = []

        if self.book is not None:
            if self.tagGuids:
                for guid in self.tagGuids:
                    name = utf8(self.book.get_tag(guid))
                    names.append(name)

        return names

    @tags.setter
    def tags(self, value):
        self._tags = value

    def html_content(self, url=None):
        if url:
            if self.attributes.sourceURL:
                if not self.attributes.sourceURL.startswith(url):
                    return True
        return False

    @property
    def encoded(self):
        if isinstance(self.title, unicode):
            self.title = string(self.title)

        if isinstance(self.content, unicode):
            self.content = string(self.content)
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


class EnStack():

    def __init__(self):
        pass

    def __iter__(self):
        # return notebooks
        pass
