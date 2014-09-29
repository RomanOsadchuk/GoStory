from json import JSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Count
from .models import Story, Chapter


class StoryService(object):
    AUTHORS_NUM = 5
    
    @classmethod
    def get_detail_context(cls, story):
        chapters = Chapter.objects.filter(story=story)
        context = {
            'chapter_num': chapters.count(),
            'authors': chapters.values('author__username').annotate(
                chap_num=Count('id')).order_by('-chap_num')[:cls.AUTHORS_NUM]
        }
        return context
    
    @classmethod
    def get_tree_json(cls, story, user):    
        chapters = Chapter.objects.filter(story=story)
        if user.is_authenticated():
            chapters.select_related('readers', 'bookmarkers', 'likers')
        nodes = []
        for c in chapters:
            parent_pk = c.parent.pk if c.parent else None
            url = reverse('read_story', kwargs={'pk': story.pk})
            url += '?chapter-pk={}'.format(c.pk)
            node = {'pk': c.pk, 'parent': parent_pk, 'title': c.headline[:20],
                    'children': [], 'url': url}
            for n in nodes:
                if n['parent'] == c.pk: node['children'].append(n)
                elif parent_pk == n['pk']: n['children'].append(node)
            nodes.append(node)
            
            # TODO: pick color in template
            if user in c.bookmarkers.all(): node['color'] = 'blue'
            elif user in c.likers.all(): node['color'] = 'red'
            elif user in c.readers.all(): node['color'] = 'green'
            else: node['color'] = 'grey'
            
            if not parent_pk:
                root = [node]
        encoder = JSONEncoder()
        return encoder.encode(root)


class ChapterService(object):

    @classmethod
    def add_feedback(cls, chapter, feedback_type, user):
        if feedback_type == 'add-bookmark':
            chapter.bookmarkers.add(user)
        elif feedback_type == 'remove-bookmark':
            chapter.bookmarkers.remove(user)
        elif feedback_type == 'like':
            chapter.likers.add(user)
        elif feedback_type == 'cancel-like':
            chapter.likers.remove(user)
        else:
            return False, {'message': 'unknown or no feedback type'}
        return True, {'message': 'OK'}

