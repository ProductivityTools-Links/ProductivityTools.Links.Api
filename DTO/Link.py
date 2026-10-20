class Link:
    def __init__(self,id,parent_id,name,description,url,authors=None):
        self.id=id
        self.parent_id=parent_id
        self.name=name
        self.description=description
        self.url=url
        self.authors=authors if isinstance(authors, list) else ([] if not authors else [authors])