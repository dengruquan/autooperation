from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.utils.decorators import method_decorator
# from guardian.decorators import permission_required_or_403
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Operator 
from .forms import OperatorForm

    
class OperatorListAll(TemplateView):
    template_name = 'cmdb/operator.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OperatorListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = {
            'op_list': Operator.objects.all()
        }
        kwargs.update(context)
        
        return super(OperatorListAll, self).get_context_data(**kwargs)
        
        
class OperatorAdd(CreateView):
    model = Operator
    form_class = OperatorForm
    template_name = 'cmdb/operator-add.html'
    success_url = reverse_lazy('cmdb:operator_list')

    # @method_decorator(login_required)
    # @method_decorator(permission_required_or_403('asset.add_asset'))
    def dispatch(self, *args, **kwargs):
        return super(OperatorAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.operator_save = operator_save = form.save()
        return super(OperatorAdd, self).form_valid(form)

    def get_success_url(self):
        return super(OperatorAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            # "asset_active": "active",
            # "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(OperatorAdd, self).get_context_data(**kwargs)

        
class OperatorDel(View):
    model = Operator

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OperatorDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            opertor_obj = Operator.objects.get(id=id)
            opertor_obj.delete()
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        return HttpResponse(json.dumps(ret))

class OperatorUpdate(UpdateView):
    model = Operator
    form_class = OperatorForm
    template_name = 'cmdb/operator-update.html'
    success_url = reverse_lazy('cmdb:operator_list')
    
    def dispatch(self, *args, **kwargs):
        return super(OperatorDel, self).dispatch(*args, **kwargs)
        
        
    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(OperatorUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(OperatorUpdate, self).form_invalid(form)

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
        return super(OperatorUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(OperatorUpdate, self).get_success_url()
        
def operator_save(request):
    if request.method == 'POST':
        operator_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        operator_item = Operator.objects.get(id=operator_id)
        
        operator_item.name = name
        operator_item.desc = desc
        operator_item.save()
        #todo
        print("name, desc,", operator_item.name, operator_item.desc)
        #end
    return HttpResponseRedirect(reverse("cmdb:operator_list"))

    
def operator_update(request, ids):
    obj = Operator.objects.get(id=ids)
    return render(request, "cmdb/operator-update.html", locals())