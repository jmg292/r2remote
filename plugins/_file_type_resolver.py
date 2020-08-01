class FileInfo(object):

    def __init__(self, file_type, extension, mime, offset, signature):
        self.type = file_type
        self.extension = extension
        self.mime_type = mime
        self.signatures = signature
