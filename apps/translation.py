from modeltranslation.translator import register , TranslationOptions
from .models import News , Category

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title' , 'content' ,'body')

@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)