class BaseEntity:
    @property
    def raw_id(self):
        raise NotImplementedError('This function need to be implemented on inherited class')

    @property
    def name(self):
        raise NotImplementedError('This function need to be implemented on inherited class')

    def __init__(self, uid, extra_relationship=None):
        self.id = uid
        self.extra_relationship = extra_relationship or []
