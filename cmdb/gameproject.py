from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.utils.decorators import method_decorator
# from guardian.decorators import permission_required_or_403
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import GameProject 
from .forms import GameProjectForm

    
class GameProjectListAll(TemplateView):
    template_name = 'cmdb/gameproject.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameProjectListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = {
            'gp_list': GameProject.objects.all()
        }
        kwargs.update(context)
        
        return super(GameProjectListAll, self).get_context_data(**kwargs)
        
        
class GameProjectAdd(CreateView):
    model = GameProject
    form_class = GameProjectForm
    template_name = 'cmdb/gameproject-add.html'
    success_url = reverse_lazy('cmdb:gameproject_list')

    # @method_decorator(login_required)
    # @method_decorator(permission_required_or_403('asset.add_asset'))
    def dispatch(self, *args, **kwargs):
        return super(GameProjectAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #todo
        print("run to here of gameproject form_valid")
        #end
        self.gameproject_save = gameproject_save = form.save()
        return super(GameProjectAdd, self).form_valid(form)

    def get_success_url(self):
       #todo
        print("run to here of gameproject get_success_url")
        #end
        return super(GameProjectAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            # "asset_active": "active",
            # "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(GameProjectAdd, self).get_context_data(**kwargs)

        
class GameProjectDel(View):
    model = GameProject

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameProjectDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            opertor_obj = GameProject.objects.get(id=id)
            opertor_obj.delete()
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        return HttpResponse(json.dumps(ret))

        
class GameProjectUpdate(UpdateView):
    model = GameProject
    form_class = GameProjectForm
    template_name = 'cmdb/gameproject-update.html'
    success_url = reverse_lazy('cmdb:gameproject_list')
    
    def dispatch(self, *args, **kwargs):
        return super(GameProjectDel, self).dispatch(*args, **kwargs)
        
        
    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(GameProjectUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(GameProjectUpdate, self).form_invalid(form)

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
        return super(GameProjectUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(GameProjectUpdate, self).get_success_url()
        
        
def gameproject_save(request):
    if request.method == 'POST':
        gp_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        gameproject_item = GameProject.objects.get(id=gp_id)
        
        gameproject_item.name = name
        gameproject_item.desc = desc
        gameproject_item.save()
    return HttpResponseRedirect(reverse("cmdb:gameproject_list"))

    
def gameproject_update(request, ids):
    obj = GameProject.objects.get(id=ids)
    return render(request, "cmdb/gameproject-update.html", locals())
    
    