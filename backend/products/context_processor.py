from products.models import products,CategoryInfo
from json import dumps

def main(request):
    titles={}
    PoultryCategoryImage=""
    PoultryCategoryInfo="Coming Soon1"
    MuttonCategoryImage=""
    MuttonCategoryInfo="Coming Soon"
    SeafoodCategoryImage=""
    SeafoodCategoryInfo="Coming Soon"

    try:
        PoultryCategory=CategoryInfo.objects.get(category='poultry')
        MuttonCategory=CategoryInfo.objects.get(category='mutton')
        SeafoodCategory=CategoryInfo.objects.get(category='seafood')

    except CategoryImages.DoesNotExist:
        pass
    else:
        PoultryCategoryImage=PoultryCategory.get_img_url()
        PoultryCategoryInfo=PoultryCategory.categoryInfo

        MuttonCategoryImage=MuttonCategory.get_img_url()
        MuttonCategoryInfo=MuttonCategory.categoryInfo

        SeafoodCategoryImage=SeafoodCategory.get_img_url()
        SeafoodCategoryInfo=SeafoodCategory.categoryInfo

    finally:
        for product in products.objects.all():
            titles[product.id]=product.title
        titles=dumps(titles)
        
        
        return {"titles":titles,'PoultryCategoryImage':PoultryCategoryImage,'MuttonCategoryImage':MuttonCategoryImage,'SeafoodCategoryImage':SeafoodCategoryImage,
        'PoultryCategoryInfo':PoultryCategoryInfo,'MuttonCategoryInfo':MuttonCategoryInfo,'SeafoodCategoryInfo':SeafoodCategoryInfo}