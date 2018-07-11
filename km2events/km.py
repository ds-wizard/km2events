
class KMPart:

    def __init__(self, uuid: str):
        self.uuid = uuid


class KnowledgeModel(KMPart):

    def __init__(self, uuid, name):
        super().__init__(uuid)
        self.everything = dict()  # type: Dict[uuid.UUID, KMPart]

        self.name = name  # type: str

        self.chapters = []  # type: List[Chapter]
        self.metrics = []  # type: List[Metric]


class Metric(KMPart):

    def __init__(self, uuid, title, abbreviation, description=None):
        super().__init__(uuid)

        self.title = title  # type: str
        self.abbreviation = abbabbreviation  # type: str
        self.description = description  # type: str

        self.references = [] # type: List[Reference]

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

    def __init__(self, uuid, label, advice=None, **kwargs):
        super().__init__(uuid)

        self.label = label  # type: str
        self.advice = advice  # type: str

        self.question = None  # type: Question
        self.followups = []  # type: List[Question]
        self.metrics = []  # type: List[MetricMeasure]

    @property
    def chapter(self):
        return self.question.chapter

    @property
    def km(self):
        return self.question.chapter.km


class MetricMeasure:

    def __init__(self, uuid, measure, weight=1.0):
        self.metric_uuid = uuid
        self.measure = measure
        self.weight = weight


class Expert(KMPart):

    def __init__(self, uuid, name, email=None, type="organisation", **kwargs):
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
