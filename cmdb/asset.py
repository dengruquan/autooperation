from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, View, DetailView, UpdateView
from django.utils.decorators import method_decorator
# from guardian.decorators import permission_required_or_403
from django.urls import reverse_lazy
from .models import Host 
from .forms import AssetForm
from common import common
from jobs import tasks


class AssetListAll(TemplateView):
    template_name = 'cmdb/asset.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = {
            'asset_list': Host.objects.all()
        }
        kwargs.update(context)
        
        return super(AssetListAll, self).get_context_data(**kwargs)
        
        
class AssetAdd(CreateView):
    model = Host
    form_class = AssetForm
    template_name = 'cmdb/asset-add.html'
    success_url = reverse_lazy('cmdb:asset_list')

    # @method_decorator(login_required)
    # @method_decorator(permission_required_or_403('asset.add_asset'))
    def dispatch(self, *args, **kwargs):
        return super(AssetAdd, self).dispatch(*args, **kwargs)
        
    def form_invalid(self, form):
        print(form.errors)
        return super(AssetAdd, self).form_invalid(form)
        
        
    def form_valid(self, form):
        self.asset_save = asset_save = form.save()

        return super(AssetAdd, self).form_valid(form)

    def get_success_url(self):
        obj = Host.objects.get(hostname= self.asset_save)
        if obj:
            print("self.asset_save", obj)

        #实现ssh免密码登录
        tasks.deal_sshkey.apply_async(
            (obj.id, obj.public_ip, obj.ssh_port, obj.user, obj.passwd, common.SSH_Command))
        return super(AssetAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            # "asset_active": "active",
            # "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(AssetAdd, self).get_context_data(**kwargs)

        
class AssetDel(View):
    model = Host

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            # user = User.objects.get(username=request.user)
            # checker = ObjectPermissionChecker(user)
            assets = Host.objects.get(id=id)
            # if checker.has_perm('delete_asset', assets, ) == True:
            assets.delete()
                # GroupObjectPermission.objects.filter(object_pk=id).delete()
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        return HttpResponse(json.dumps(ret))


class AssetDetail(DetailView):
    model = Host
    template_name = 'cmdb/asset-detail.html'

    # @method_decorator(login_required)
    # @method_decorator(permission_required_or_403('asset.change_asset', (asset, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(AssetDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = Host.objects.get(id=pk)

        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "assets": detail,
            "nid": pk,
            "a_form": AssetForm(instance=detail),
        }
        kwargs.update(context)
        return super(AssetDetail, self).get_context_data(**kwargs)

        
class AssetUpdate(UpdateView):
    model = Host
    form_class = AssetForm
    template_name = 'cmdb/asset-update.html'
    success_url = reverse_lazy('cmdb:asset_list')

    # @method_decorator(login_required)
    # @method_decorator(permission_required_or_403('asset.add_asset', (asset, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(AssetUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(AssetUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(AssetUpdate, self).form_invalid(form)

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
        return super(AssetUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(AssetUpdate, self).get_success_url()


def asset_hardware_update(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        try:
            id = request.POST.get('nid', None)
            obj = Host.objects.get(id=id)
            ip = obj.public_ip
            port = obj.ssh_port
            # username = obj.user
            # password1 = obj.passwd
            username = ""
            password = ""

            tasks.run(id, ip, port, username, password)
        except:
            print("asset_hardware_update error") 
            pass
           
    return HttpResponse(json.dumps(ret))