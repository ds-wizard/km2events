from km2events.km import KnowledgeModel, Chapter, Question, \
                         Answer, Expert, Reference, KMPart, \
                         MetricMeasure, Metric
from km2events.exceptions import UUIDDuplicityError, UnknownUUIDError


class CoreLoader:

    def __init__(self, **kwargs):
        self.uuid_registry = dict()

        self.km = KnowledgeModel(**kwargs)
        self._register_obj(self.km)

    @staticmethod
    def create_from_package(package_data):
        loader = CoreLoader(**package_data)
        loader.km.metrics = [
            Metric(**metric_data)
            for metric_data in package_data.get('metrics', [])
        ]
        return loader

    def add_chapter(self, chapter_data):
        preconditions = dict()  # UUID: UUID

        chapter = Chapter(**chapter_data)
        chapter.km = self.km
        self.km.chapters.append(chapter)
        for question_data in chapter_data.get('questions', []):
            self._add_question(chapter, question_data, preconditions)

        for followup_uuid, precondition_uuid in preconditions.items():
            followup = self.uuid_registry.get(followup_uuid, None)
            precondition = self.uuid_registry.get(precondition_uuid, None)
            if precondition is None:  # followup cannot be None
                raise UnknownUUIDError(precondition_uuid)

            followup.precondition = precondition
            precondition.followups.append(followup)

        self.km.everything = self.uuid_registry

    def _add_question(self, chapter: Chapter, question_data, preconditions):
        question = Question(**question_data)
        question.chapter = chapter
        chapter.questions.append(question)
        self._register_obj(question)

        if 'precondition' in question_data:
            preconditions[question.uuid] = question_data['precondition']
        for answer_data in question_data.get('answers', []):
            self._add_answer(question, answer_data)
        for expert_data in question_data.get('experts', []):
            self._add_expert(question, expert_data)
        for reference_data in question_data.get('references', []):
            self._add_reference(question, reference_data)

    def _add_answer(self, question: Question, answer_data):
        answer = Answer(**answer_data)
        answer.question = question
        question.answers.append(answer)
        self._register_obj(answer)

        for metric_data in answer_data.get('metrics', []):
            self._add_metric_measure(answer, metric_data)

    def _add_metric_measure(self, answer: Answer, metric_data):
        metric_measure = MetricMeasure(**metric_data)
        answer.metrics.append(metric_measure)

    def _add_expert(self, question: Question, expert_data):
        expert = Expert(**expert_data)
        expert.question = question
        question.experts.append(expert)
        self._register_obj(expert)

    def _add_reference(self, question: Question, reference_data):
        reference = Reference(**reference_data)
        reference.question = question
        question.references.append(reference)
        self._register_obj(reference)

    def _register_obj(self, obj: KMPart):
        if obj.uuid in self.uuid_registry:
            raise UUIDDuplicityError(obj.uuid)
        self.uuid_registry[obj.uuid] = obj
