
class KMPart:

    def __init__(self, uuid: str):
        self.uuid = uuid


class KnowledgeModel(KMPart):

    def __init__(self, uuid, name):
        super().__init__(uuid)
        self.everything = dict()  # type: Dict[uuid.UUID, KMPart]

        self.name = name  # type: str

        self.chapters = []  # type: List[Chapter]


class Chapter(KMPart):

    def __init__(self, uuid, title, text="", **kwargs):
        super().__init__(uuid)

        self.title = title  # type: str
        self.text = text  # type: str

        self.questions = []  # type: List[Question]
        self.km = None  # type: KnowledgeModel


class Question(KMPart):

    def __init__(self, uuid, type, title, text="", **kwargs):
        super().__init__(uuid)

        self.type = type  # type: str
        self.title = title  # type: str
        self.text = text  # type: str

        self.precondition = None  # type: Answer
        self.followups = []  # type: List[Question]
        self.answers = []  # type: List[Answer]
        self.experts = []  # type: List[Expert]
        self.references = []  # type: List[Reference]
        self.chapter = None  # type: Chapter

    @property
    def is_followup(self):
        return self.precondition is not None

    @property
    def is_root(self):
        return self.precondition is None

    @property
    def km(self):
        return self.chapter.km


class Answer(KMPart):

    def __init__(self, uuid, label, advice="", **kwargs):
        super().__init__(uuid)

        self.label = label  # type: str
        self.advice = advice  # type: str

        self.question = None  # type: Question
        self.followups = []  # type: List[Question]

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km


class Expert(KMPart):

    def __init__(self, uuid, name, email="", type="organisation", **kwargs):
        super().__init__(uuid)

        self.name = name  # type: str
        self.email = email  # type: str
        self.type = type  # type: str

        self.question = None  # type: Question

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km


class Reference(KMPart):

    def __init__(self, uuid, type, **kwargs):
        super().__init__(uuid)

        self.type = type  # type: str
        self.content = dict(kwargs)  # type: Dict[str, str]

        self.question = None  # type: Question

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km
