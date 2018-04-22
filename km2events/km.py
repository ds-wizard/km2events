

class KMPart:

    def __init__(self, uuid):
        self.uuid = uuid


class KnowledgeModel(KMPart):

    def __init__(self, uuid, name):
        super().__init__(uuid)

        self.name = name

        self.chapters = []


class Chapter(KMPart):

    def __init__(self, uuid, title, text="", **kwargs):
        super().__init__(uuid)

        self.title = title
        self.text = text

        self.questions = []
        self.km = None


class Question(KMPart):

    def __init__(self, uuid, type, title, text="", **kwargs):
        super().__init__(uuid)

        self.type = type
        self.title = title
        self.text = text

        self.precondition = None
        self.followups = []
        self.answers = []
        self.experts = []
        self.references = []
        self.chapter = None

    @property
    def is_followup(self):
        return self.precondition is not None

    @property
    def km(self):
        return self.chapter.km


class Answer(KMPart):

    def __init__(self, uuid, label, advice="", **kwargs):
        super().__init__(uuid)

        self.label = label
        self.advice = advice

        self.question = None
        self.followups = []

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km


class Expert(KMPart):

    def __init__(self, uuid, name, email="", type="organisation", **kwargs):
        super().__init__(uuid)

        self.name = name
        self.email = email
        self.type = type

        self.question = None

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km


class Reference(KMPart):

    def __init__(self, uuid, type, **kwargs):
        super().__init__(uuid)

        self.type = type
        self.content = dict(kwargs)

        self.question = None

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km


