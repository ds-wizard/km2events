from km2events.km import KnowledgeModel, Chapter, Question, \
                         Answer, Expert, Reference
from km2events.uuid import UUIDGenerator


class EventsBuilder:

    def __init__(self):
        self.events = []
        self.km = None
        self._uuid_generator = UUIDGenerator()

    @staticmethod
    def _construct_path(breadcrumbs: list) -> list:
        return [
            {'type': t, 'uuid': u} for t, u in breadcrumbs
        ]

    def add_km(self, km: KnowledgeModel):
        self.km = km
        self.events.append({
            'eventType': 'AddKnowledgeModelEvent',
            'uuid': self._uuid_generator.generate(),
            'path': self._construct_path([]),
            'kmUuid': km.uuid,
            'name': km.name
        })

        for chapter in km.chapters:
            self._add_chapter(chapter)

    def _add_chapter(self, chapter: Chapter):
        breadcrumbs = [('km', chapter.km.uuid)]
        event = {
            'eventType': 'AddChapterEvent',
            'uuid': self._uuid_generator.generate(),
            'path': self._construct_path(breadcrumbs),
            'chapterUuid': chapter.uuid,
            'title': chapter.title,
            'text': chapter.text
        }
        self.events.append(event)

        breadcrumbs.append(('chapter', chapter.uuid))
        for question in chapter.questions:
            if question.is_root:
                self._add_question(question, breadcrumbs)

    def _add_question(self, question: Question, breadcrumbs: list):
        qtype = question.type
        if qtype == 'option':
            qtype = 'options'
        requiredLevel = question.phase
        if requiredLevel == 4:  # i.e. never
            requiredLevel = None
        event = {
            'eventType': 'AddQuestionEvent',
            'uuid': self._uuid_generator.generate(),
            'path': self._construct_path(breadcrumbs),
            'questionUuid': question.uuid,
            'requiredLevel': requiredLevel,
            'type': qtype,
            'title': question.title,
            'text': question.text,
            'answerItemTemplate': None
        }
        if question.type == 'list':
            event['answerItemTemplate'] = {"title": "Item"}

        self.events.append(event)

        xbreadcrumbs = list(breadcrumbs)
        xbreadcrumbs.append(('question', question.uuid))
        for expert in question.experts:
            self._add_expert(expert, xbreadcrumbs)
        for reference in question.references:
            self._add_reference(reference, xbreadcrumbs)
        for answer in question.answers:
            self._add_answer(answer, xbreadcrumbs)
        if question.type == 'list':
            for followup in question.followups:
                self._add_question(followup, xbreadcrumbs)
        elif len(question.followups) > 0:  # followups on other types -> after
            xbreadcrumbs = xbreadcrumbs[:-1]
            for followup in question.followups:
                self._add_question(followup, xbreadcrumbs)

    def _add_answer(self, answer: Answer, breadcrumbs: list):
        event = {
            'eventType': 'AddAnswerEvent',
            'uuid': self._uuid_generator.generate(),
            'path': self._construct_path(breadcrumbs),
            'answerUuid': answer.uuid,
            'label': answer.label,
            'advice': answer.advice,
            'metricMeasures': [
                {
                    'metricUuid': metric_measure.metric_uuid,
                    'measure': metric_measure.measure,
                    'weight': metric_measure.weight
                }
                for metric_measure in answer.metrics
            ]
        }
        self.events.append(event)

        xbreadcrumbs = list(breadcrumbs)
        xbreadcrumbs.append(('answer', answer.uuid))
        for followup in answer.followups:
            self._add_question(followup, xbreadcrumbs)

    def _add_expert(self, expert: Expert, breadcrumbs: list):
        event = {
            'eventType': 'AddExpertEvent',
            'uuid': self._uuid_generator.generate(),
            'path': self._construct_path(breadcrumbs),
            'expertUuid': expert.uuid,
            'name': expert.name,
            'email': expert.email
        }
        self.events.append(event)

    def _add_reference(self, reference: Reference, breadcrumbs: list):
        types = {
            'url': 'URLReference',
            'xref': 'CrossReference',
            'resourcepage': 'ResourcePageReference'
        }
        if reference.type == 'dmpbook':
            return
        event = {
            'eventType': 'AddReferenceEvent',
            'referenceType': types[reference.type],
            'uuid': self._uuid_generator.generate(),
            'path': self._construct_path(breadcrumbs),
            'referenceUuid': reference.uuid
        }
        if reference.type == 'url':
            event['url'] = reference.content['weblink']
            event['label'] = reference.content.get('anchor', event['url'])
        elif reference.type == 'xref':
            event['targetUuid'] = reference.content['target']
            event['description'] = reference.content['description']
        elif reference.type == 'resourcepage':
            event['shortUuid'] = reference.content['shortuid']
        self.events.append(event)

    def make_package(self, name, version, kmId, organizationId,
                     description='Transformed by km2events',
                     parentPackageId=None):
        return {
            'parentPackageId': parentPackageId,
            'kmId': kmId,
            'name': name,
            'version': version,
            'organizationId': organizationId,
            'id': '{}:{}:{}'.format(organizationId, kmId, version),
            'description': description,
            'events': self.events
        }
