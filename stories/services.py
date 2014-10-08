from json import JSONEncoder
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count
from .models import Story, Chapter


class StoryService(object):
    ORDER_RECENT = 'recent'
    ORDER_OLD = 'old'
    ORDERINGS = {
        ORDER_RECENT: '-started_at',
        ORDER_OLD: 'started_at',
    }
    DEFAULT_ORDERING = '-started_at'
    AUTHORS_NUM = 5
    
    @classmethod
    def get_story_list(cls, title=None, ordering=None, limit=None,
            **ignore_other_params):
        stories = Story.objects.all()
        if title:
            stories = stories.filter(title__icontains=title)
        order = cls.ORDERINGS.get(ordering, cls.DEFAULT_ORDERING)
        stories = stories.order_by(order)
        if limit:
            stories = stories[:limit]
        return stories
    
    @classmethod
    def get_recent(cls, limit):
        return cls.get_story_list(ordering=cls.ORDER_RECENT, limit=limit)
    
    @classmethod
    def get_interesting(cls, limit):
        # TODO: make it realy interesting
        return cls.get_story_list(ordering=cls.ORDER_OLD, limit=limit)
    
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


class AuthorService(object):
    ORDER_NAME = 'username'
    ORDER_CHAP_NUM = 'chapters_number'
    ORDERINGS = {
        ORDER_NAME: 'username',
        ORDER_CHAP_NUM: '-chap_num',
    }
    DEFAULT_ORDERING = 'username'
    
    @classmethod
    def get_author_list(cls, name=None, ordering=None, limit=None,
            **ignore_other_params):
        authors = User.objects.annotate(chap_num=Count('chapter'))
        authors = authors.filter(is_staff=False, chap_num__gt=0)
        if name:
            authors = authors.filter(username__icontains=name)
        order = cls.ORDERINGS.get(ordering, cls.DEFAULT_ORDERING)
        authors = authors.order_by(order)
        if limit:
            authors = authors[:limit]
        return authors
    
    @classmethod
    def get_most_writable(cls, limit):
        return cls.get_author_list(ordering=cls.ORDER_CHAP_NUM, limit=limit)

