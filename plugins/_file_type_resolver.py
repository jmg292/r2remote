class FileInfo(object):

    def __init__(self, type, extension, mime, offset, signature):
        self.type = type
        self.extension = extension
        self.mime_type = mime
        self.signatures = signature
