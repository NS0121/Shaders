from pickle import FALSE, TRUE
import unreal

editor_util = unreal.GlobalEditorUtilityBase.get_default_object()
assets = editor_util.get_selected_assets()

materials = unreal.EditorFilterLibrary.by_class(assets, unreal.Material)

#マテリアルのみを取得する
for material in materials:

#宣言

#上端
    #影の色
    ShadowColor = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionVectorParameter,-738,135)
    ShadowColor.set_editor_property("parameter_name","ShadowColor")

    #テクスチャーサンプル
    TextureSample = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionVectorParameter,-738,350)
    TextureSample.set_editor_property("parameter_name","TextureSample")
    
    #Lerp
    Lerp = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionLinearInterpolate,-256,150)

    #影の色とテクスチャーを混ぜるMultiply
    ShadowMultiply = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionMultiply,-512,150)

#下端
    #Clamp
    Clamp = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionClamp,-512,600)

    #内積結果を倍増させるMultiply
    DoubleMultiply = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionMultiply,-738,600)
    DoubleMultiply.set_editor_property("const_b",10.0)

    #Add
    SetAdd_1 = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionAdd,-1024,400)
    SetAdd_2 = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionAdd,-864,600)

    #再結合用Multiply
    Multiply_R = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionMultiply,-1360,400)
    Multiply_G = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionMultiply,-1360,600)
    Multiply_B = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionMultiply,-1360,800)

    #Mask
    SunMask_R = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionComponentMask,-1616,400)
    SunMask_R.set_editor_property("r",True)
    SunMask_R.set_editor_property("g",False)
    SunMask_R.set_editor_property("b",False)

    SunMask_G = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionComponentMask,-1616,550)
    SunMask_G.set_editor_property("r",False)
    SunMask_G.set_editor_property("g",True)
    SunMask_G.set_editor_property("b",False)
    
    SunMask_B = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionComponentMask,-1616,700)
    SunMask_B.set_editor_property("r",False)
    SunMask_B.set_editor_property("g",False)
    SunMask_B.set_editor_property("b",True)

    NormalMask_R = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionComponentMask,-1616,900)
    NormalMask_R.set_editor_property("r",True)
    NormalMask_R.set_editor_property("g",False)
    NormalMask_R.set_editor_property("b",False)

    NormalMask_G = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionComponentMask,-1616,1050)
    NormalMask_G.set_editor_property("r",False)
    NormalMask_G.set_editor_property("g",True)
    NormalMask_G.set_editor_property("b",False)

    NormalMask_B = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionComponentMask,-1616,1200)
    NormalMask_B.set_editor_property("r",False)
    NormalMask_B.set_editor_property("g",False)
    NormalMask_B.set_editor_property("b",True)

    #DirectionLightの情報を取得
    DirecitonLightVector = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionSkyAtmosphereLightDirection,-1900,400)

    #モデルの法線情報を取得
    ModelVector = unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionVertexNormalWS,-1900,900)


#接続
# unreal.MaterialEditingLibrary.connect_material_expressions(接続の子,"",接続元,"接続する場所")
    #本体に接続
    unreal.MaterialEditingLibrary.connect_material_property(Lerp,"",unreal.MaterialProperty.MP_EMISSIVE_COLOR)

    #テクスチャー
    unreal.MaterialEditingLibrary.connect_material_expressions(ShadowMultiply,"",Lerp,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(ShadowColor,"",ShadowMultiply,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(TextureSample,"",Lerp,"B")
    unreal.MaterialEditingLibrary.connect_material_expressions(TextureSample,"",ShadowMultiply,"B")

    #陰影処理
        #処理結果を元に表示形式を設定
    unreal.MaterialEditingLibrary.connect_material_expressions(Clamp,"",Lerp,"Alpha")
    unreal.MaterialEditingLibrary.connect_material_expressions(DoubleMultiply,"",Clamp,"")
    unreal.MaterialEditingLibrary.connect_material_expressions(SetAdd_2,"",DoubleMultiply,"A")

        #結果を結合
    unreal.MaterialEditingLibrary.connect_material_expressions(SetAdd_1,"",SetAdd_2,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(Multiply_B,"",SetAdd_2,"B")
    unreal.MaterialEditingLibrary.connect_material_expressions(Multiply_R,"",SetAdd_1,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(Multiply_G,"",SetAdd_1,"B")

        #各ベクトルごとに計算
    unreal.MaterialEditingLibrary.connect_material_expressions(SunMask_R,"",Multiply_R,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(NormalMask_R,"",Multiply_R,"B")
    unreal.MaterialEditingLibrary.connect_material_expressions(SunMask_G,"",Multiply_G,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(NormalMask_G,"",Multiply_G,"B")
    unreal.MaterialEditingLibrary.connect_material_expressions(SunMask_B,"",Multiply_B,"A")
    unreal.MaterialEditingLibrary.connect_material_expressions(NormalMask_B,"",Multiply_B,"B")
    
        #ライトの各ベクトルを取得
    unreal.MaterialEditingLibrary.connect_material_expressions(DirecitonLightVector,"",SunMask_R,"")
    unreal.MaterialEditingLibrary.connect_material_expressions(DirecitonLightVector,"",SunMask_G,"")
    unreal.MaterialEditingLibrary.connect_material_expressions(DirecitonLightVector,"",SunMask_B,"")
    
        #ライトの各ベクトルを取得
    unreal.MaterialEditingLibrary.connect_material_expressions(ModelVector,"",NormalMask_R,"")
    unreal.MaterialEditingLibrary.connect_material_expressions(ModelVector,"",NormalMask_G,"")
    unreal.MaterialEditingLibrary.connect_material_expressions(ModelVector,"",NormalMask_B,"")
    

    
