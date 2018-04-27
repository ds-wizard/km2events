from km2events.km import KnowledgeModel, Chapter, Question, \
                         Answer, Expert, Reference
from km2events.uuid import UUIDGenerator


class EventsBuilder:

    def __init__(self):
        self.events = []
        self.km = None
        self._uuid_generator = UUIDGenerator()

    def add_km(self, km: KnowledgeModel):
        self.km = km
        self.events.append({
            'eventType': 'AddKnowledgeModelEvent',
            'uuid': self._uuid_generator.generate(),
            'kmUuid': km.uuid,
            'name': km.name
        })

        for chapter in km.chapters:
            self._add_chapter(chapter)

    def _add_chapter(self, chapter: Chapter):
        event = {
            'eventType': 'AddChapterEvent',
            'uuid': self._uuid_generator.generate(),
            'kmUuid': chapter.km.uuid,
            'chapterUuid': chapter.uuid,
            'title': chapter.title,
            'text': chapter.text
        }
        self.events.append(event)

        for question in chapter.questions:
            if question.is_root:
                self._add_question(question)

    def _add_question(self, question: Question, parent=None):
        event_type = 'AddQuestionEvent' if parent is None else 'AddFollowUpQuestionEvent'
        event = {
            'eventType': event_type,
            'uuid': self._uuid_generator.generate(),
            'kmUuid': question.km.uuid,
            'chapterUuid': question.chapter.uuid,
            'questionUuid': question.uuid,
            'type': question.type,
            'title': question.title,
            'text': question.text,
            'shortQuestionUuid': None,
            'answerItemTemplate': None
        }
        if parent is not None:
            event['answerUuid'] = parent.uuid
        self.events.append(event)

        for expert in question.experts:
            self._add_expert(expert)
        for reference in question.references:
            self._add_reference(reference)
        for answer in question.answers:
            self._add_answer(answer)

    def _add_answer(self, answer: Answer):
        event = {
            'eventType': 'AddAnswerEvent',
            'uuid': self._uuid_generator.generate(),
            'kmUuid': answer.km.uuid,
            'chapterUuid': answer.chapter.uuid,
            'questionUuid': answer.question.uuid,
            'answerUuid': answer.uuid,
            'label': answer.label,
            'advice': answer.advice
        }
        self.events.append(event)

        for followup in answer.followups:
            self._add_question(followup, answer)

    def _add_expert(self, expert: Expert):
        event = {
            'eventType': 'AddExpertEvent',
            'uuid': self._uuid_generator.generate(),
            'kmUuid': expert.km.uuid,
            'chapterUuid': expert.chapter.uuid,
            'questionUuid': expert.question.uuid,
            'expertUuid': expert.uuid,
            'name': expert.name,
            'email': expert.email
        }
        self.events.append(event)

    def _add_reference(self, reference: Reference):
        if reference.type != 'dmpbook':  # current DSW knows only dmpbook
            return
        event = {
            'eventType': 'AddReferenceEvent',
            'uuid': self._uuid_generator.generate(),
            'kmUuid': reference.km.uuid,
            'chapterUuid': reference.chapter.uuid,
            'questionUuid': reference.question.uuid,
            'referenceUuid': reference.uuid,
            'chapter': reference.content['chapter']
        }
        self.events.append(event)

    def make_package(self, name, version, artifactId, groupId,
                     description='Transformed by km2events',
                     parentPackageId=None):
        return {
            'parentPackageId': parentPackageId,
            'artifactId': artifactId,
            'name': name,
            'version': version,
            'groupId': groupId,
            'id': '{}:{}'.format(groupId, version),
            'description': description,
            'events': self.events
        }
