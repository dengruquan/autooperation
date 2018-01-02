from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.utils.decorators import method_decorator
# from guardian.decorators import permission_required_or_403
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import GameVersion
from .forms import GameVersionForm

    
class GameVersionListAll(TemplateView):
    template_name = 'cmdb/gameversion.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameVersionListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = {
            'gv_list': GameVersion.objects.all()
        }
        kwargs.update(context)
        
        return super(GameVersionListAll, self).get_context_data(**kwargs)
        
        
class GameVersionAdd(CreateView):
    model = GameVersion
    form_class = GameVersionForm
    template_name = 'cmdb/gameversion-add.html'
    success_url = reverse_lazy('cmdb:gameversion_list')

    # @method_decorator(login_required)
    # @method_decorator(permission_required_or_403('asset.add_asset'))
    def dispatch(self, *args, **kwargs):
        return super(GameVersionAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #todo
        print("run to here of gameversion form_valid")
        #end
        self.gameversion_save = gameversion_save = form.save()
        return super(GameVersionAdd, self).form_valid(form)
        
    def http_method_not_allowed(self, *args, **kwargs):
        return super(GameVersionAdd, self).http_method_not_allowed(*args, **kwargs) 

    def get_success_url(self):
       #todo
        print("run to here of gameversion get_success_url")
        #end
        return super(GameVersionAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            # "asset_active": "active",
            # "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(GameVersionAdd, self).get_context_data(**kwargs)

        
class GameVersionDel(View):
    model = GameVersion

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameVersionDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            opertor_obj = GameVersion.objects.get(id=id)
            opertor_obj.delete()
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        return HttpResponse(json.dumps(ret))

        
class GameVersionUpdate(UpdateView):
    model = GameVersion
    form_class = GameVersionForm
    template_name = 'cmdb/gameversion-update.html'
    success_url = reverse_lazy('cmdb:gameversion_list')
    
    def dispatch(self, *args, **kwargs):
        return super(GameVersionDel, self).dispatch(*args, **kwargs)
        
        
    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(GameVersionUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(GameVersionUpdate, self).form_invalid(form)

    def form_valid(self, form):
        # pk = self.kwargs.get(self.pk_url_kwarg, None)
        # oldmyproduct = asset.objects.get(id=pk).product_line
        # oldmygroup = Group.objects.get(name=oldmyproduct)
        self.object = form.save()
        # myproduct = asset.objects.get(id=pk).product_line
        # mygroup = Group.objects.get(name=myproduct)

        # if oldmygroup != mygroup:
            # GroupObjectPermission.objects.filter(object_pk=pk).delete()
            # GroupObjectPermission.objects.assign_perm("read_asset", mygroup, obj=self.object)
            # GroupObjectPermission.objects.assign_perm("add_asset", mygroup, obj=self.object)
            # GroupObjectPermission.objects.assign_perm("change_asset", mygroup, obj=self.object)
            # GroupObjectPermission.objects.assign_perm("delete_asset", mygroup, obj=self.object)
        return super(GameVersionUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(GameVersionUpdate, self).get_success_url()
        
        
def gameversion_save(request):
    if request.method == 'POST':
        gv_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        gameversion_item = GameVersion.objects.get(id=gv_id)
        
        gameversion_item.name = name
        gameversion_item.desc = desc
        gameversion_item.save()
    return HttpResponseRedirect(reverse("cmdb:gameversion_list"))

    
def gameversion_update(request, ids):
    obj = GameVersion.objects.get(id=ids)
    return render(request, "cmdb/gameversion-update.html", locals())
    
    