from pickle import FALSE, TRUE
import unreal

editor_util = unreal.GlobalEditorUtilityBase.get_default_object()
assets = editor_util.get_selected_assets()

materials = unreal.EditorFilterLibrary.by_class(assets, unreal.Material)
print(unreal.MaterialShadingModel.MSM_UNLIT)
#マテリアルのみを取得する
for material in materials:
    