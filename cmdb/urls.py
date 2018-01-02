from django.urls import path
from . import asset, views, operator, gameproject, gameversion

app_name = "cmdb"
urlpatterns = [
    path('', asset.AssetListAll.as_view(), name = "asset_list"),
    path('asset.html', asset.AssetListAll.as_view(), name = "asset_list"),
    path("asset-add.html", asset.AssetAdd.as_view(), name = "asset_add"),
    path("asset-del.html", asset.AssetDel.as_view(), name = "asset_del"),
    path('asset-detail-<int:pk>.html',asset.AssetDetail.as_view() ,name='asset_detail'),
    path('asset-export.html',views.export,name='asset_export'),
    path('asset-update-<int:pk>.html', asset.AssetUpdate.as_view(), name='asset_update'),
    
    path('operator.html', operator.OperatorListAll.as_view(), name = "operator_list"),
    path("operator-add.html", operator.OperatorAdd.as_view(), name = "operator_add"),
    path("operator-del.html", operator.OperatorDel.as_view(), name = "operator_del"),
    path("operator-update.html/<int:ids>", operator.operator_update, name = "operator_update"),
    path("operator-save", operator.operator_save, name = "operator_save"),
    
    path('gameproject.html', gameproject.GameProjectListAll.as_view(), name = "gameproject_list"),
    path("gameproject-add.html", gameproject.GameProjectAdd.as_view(), name = "gameproject_add"),
    path("gameproject-del.html", gameproject.GameProjectDel.as_view(), name = "gameproject_del"),
    path("gameproject-update.html/<int:ids>", gameproject.gameproject_update, name = "gameproject_update"),
    path("gameproject-save", gameproject.gameproject_save, name = "gameproject_save"),
    
    path('gameversion.html', gameversion.GameVersionListAll.as_view(), name = "gameversion_list"),
    path("gameversion-add.html", gameversion.GameVersionAdd.as_view(), name = "gameversion_add"),
    path("gameversion-del.html", gameversion.GameVersionDel.as_view(), name = "gameversion_del"),
    path("gameversion-update.html/<int:ids>", gameversion.gameversion_update, name = "gameversion_update"),
    path("gameversion-save", gameversion.gameversion_save, name = "gameversion_save"),


]