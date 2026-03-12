class SessionStore:

    def __init__(self):
        self.raw_input             = None
        self.format_requirement    = None
        self.schema                = None
        self.req_confirmed         = False
        self.schema_confirmed      = False

    def reset_requirement(self):
        self.format_requirement = None
        self.req_confirmed = False

    def reset_schema(self):
        self.schema    = None
        self.schema_confirmed = False

    def reset_all(self):
        self.__init__()


session_store = SessionStore()